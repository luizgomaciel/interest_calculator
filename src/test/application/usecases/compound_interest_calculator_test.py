import pytest
from src.python.application.usecases.compound_interest_calculator import SimulateInvestmentUseCase
from src.python.application.domain.simulation_result import (
    Investment,
    CompoundingFrequency,
    Contribution
)
from src.python.application.domain.full_simulation_report import FullSimulationReport, SimulationSummary
from src.python.application.domain.monthly_summary import MonthlySummary
from src.python.application.domain.year_summary import YearSummary


def print_simulation_report(report: FullSimulationReport, title: str = "RELATÓRIO DE SIMULAÇÃO"):
    """Imprime o relatório de simulação formatado para análise"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

    # Resumo
    print("\n📊 RESUMO DA SIMULAÇÃO")
    print("-" * 40)
    print(f"  💰 Saldo Final:           R$ {report.summary.final_balance:,.2f}")
    print(f"  💵 Total Investido:       R$ {report.summary.total_invested:,.2f}")
    print(f"  📈 Total de Juros:        R$ {report.summary.total_interest:,.2f}")
    print(f"  💳 Total de Depósitos:    R$ {report.summary.total_deposits:,.2f}")
    print(f"  📉 Taxa Efetiva Anual:    {report.summary.effective_annual_rate * 100:.2f}%")
    print(f"  🎯 Rendimento Total:      {(report.summary.total_interest / report.summary.total_invested) * 100:.2f}%")

    # Evolução Anual
    print("\n📅 EVOLUÇÃO ANUAL")
    print("-" * 80)
    print(f"{'Ano':<6}{'Saldo Inicial':>18}{'Saldo Final':>18}{'Depósitos':>15}{'Juros Ano':>15}{'Juros Total':>15}")
    print("-" * 80)
    for year in report.yearly_evolution:
        print(f"{year.year:<6}{year.initial_balance:>18,.2f}{year.final_balance:>18,.2f}"
              f"{year.deposits_this_year:>15,.2f}{year.interest_this_year:>15,.2f}{year.interest_total:>15,.2f}")

    # Evolução Mensal (mostra apenas alguns meses para não poluir)
    print("\n📆 EVOLUÇÃO MENSAL (primeiros 6 e últimos 6 meses)")
    print("-" * 100)
    print(f"{'Mês':<6}{'Saldo Inicial':>18}{'Saldo Final':>18}{'Depósito':>15}{'Juros Mês':>15}{'Juros Acum.':>15}")
    print("-" * 100)

    months_to_show = []
    if len(report.monthly_evolution) <= 12:
        months_to_show = report.monthly_evolution
    else:
        months_to_show = report.monthly_evolution[:6]
        months_to_show.append(None)  # Marcador para "..."
        months_to_show.extend(report.monthly_evolution[-6:])

    for month in months_to_show:
        if month is None:
            print(f"{'...':<6}{'...':>18}{'...':>18}{'...':>15}{'...':>15}{'...':>15}")
        else:
            print(f"{month.month:<6}{month.initial_balance:>18,.2f}{month.final_balance:>18,.2f}"
                  f"{month.deposits_this_month:>15,.2f}{month.interest_this_month:>15,.2f}{month.interest_total:>15,.2f}")

    print("=" * 80)
    print("\n")


class TestSimulateInvestmentUseCase:
    """Testes integrados para o SimulateInvestmentUseCase"""

    @pytest.fixture
    def use_case(self) -> SimulateInvestmentUseCase:
        return SimulateInvestmentUseCase()

    def test_execute_simple_investment_without_contribution(self, use_case: SimulateInvestmentUseCase):
        """Testa uma simulação simples sem aportes mensais"""
        # Arrange
        investment = Investment(
            principal=1000.0,
            annual_rate=0.12,  # 12% ao ano
            total_periods=12,  # 12 meses
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert isinstance(result, FullSimulationReport)
        assert result.summary is not None
        assert result.yearly_evolution is not None
        assert result.monthly_evolution is not None

        # Verifica o resumo
        assert result.summary.total_invested == 1000.0
        assert result.summary.final_balance > 1000.0
        assert result.summary.total_interest > 0
        assert result.summary.total_deposits == 0.0

        # Verifica evolução mensal
        assert len(result.monthly_evolution) == 12

        # Verifica evolução anual
        assert len(result.yearly_evolution) == 1

    def test_execute_investment_with_monthly_contribution(self, use_case: SimulateInvestmentUseCase):
        """Testa uma simulação com aportes mensais"""
        # Arrange
        contribution = Contribution(
            amount=100.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=1000.0,
            annual_rate=0.12,  # 12% ao ano
            total_periods=12,  # 12 meses
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert result.summary.total_invested == 1000.0 + (100.0 * 12)
        assert result.summary.total_deposits == 1200.0
        assert result.summary.final_balance > result.summary.total_invested
        assert result.summary.total_interest > 0

        # Verifica que cada mês tem depósito
        for monthly in result.monthly_evolution:
            assert monthly.deposits_this_month == 100.0

    def test_execute_investment_over_multiple_years(self, use_case: SimulateInvestmentUseCase):
        """Testa uma simulação que abrange múltiplos anos"""
        # Arrange
        contribution = Contribution(
            amount=500.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=10000.0,
            annual_rate=0.10,  # 10% ao ano
            total_periods=36,  # 3 anos
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert len(result.monthly_evolution) == 36
        assert len(result.yearly_evolution) == 3

        # Verifica evolução anual
        for i, year_summary in enumerate(result.yearly_evolution):
            assert year_summary.year == i + 1
            assert year_summary.interest_this_year > 0
            assert year_summary.deposits_this_year == 500.0 * 12

    def test_monthly_evolution_has_correct_progression(self, use_case: SimulateInvestmentUseCase):
        """Verifica se a evolução mensal tem progressão correta"""
        # Arrange
        investment = Investment(
            principal=1000.0,
            annual_rate=0.12,
            total_periods=6,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        previous_balance = 0.0
        for monthly in result.monthly_evolution:
            assert monthly.initial_balance == previous_balance
            assert monthly.final_balance > monthly.initial_balance
            assert monthly.interest_this_month > 0
            previous_balance = monthly.final_balance

    def test_accumulated_interest_is_correct(self, use_case: SimulateInvestmentUseCase):
        """Verifica se os juros acumulados estão corretos"""
        # Arrange
        investment = Investment(
            principal=5000.0,
            annual_rate=0.06,
            total_periods=12,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        total_interest_from_monthly = sum(m.interest_this_month for m in result.monthly_evolution)
        assert abs(total_interest_from_monthly - result.summary.total_interest) < 0.01

        # Verifica acumulado no último mês
        last_month = result.monthly_evolution[-1]
        assert abs(last_month.interest_total - result.summary.total_interest) < 0.01

    def test_yearly_summary_matches_monthly_aggregation(self, use_case: SimulateInvestmentUseCase):
        """Verifica se o resumo anual corresponde à agregação mensal"""
        # Arrange
        contribution = Contribution(
            amount=200.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=10000.0,
            annual_rate=0.08,
            total_periods=24,  # 2 anos
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        first_year = result.yearly_evolution[0]
        first_12_months = result.monthly_evolution[:12]

        # Total de juros do primeiro ano
        interest_year_1 = sum(m.interest_this_month for m in first_12_months)
        assert abs(first_year.interest_this_year - interest_year_1) < 0.01

        # Total de depósitos do primeiro ano
        deposits_year_1 = sum(m.deposits_this_month for m in first_12_months)
        assert abs(first_year.deposits_this_year - deposits_year_1) < 0.01

    def test_effective_annual_rate_is_calculated(self, use_case: SimulateInvestmentUseCase):
        """Verifica se a taxa efetiva anual é calculada"""
        # Arrange
        investment = Investment(
            principal=10000.0,
            annual_rate=0.12,
            total_periods=12,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert result.summary.effective_annual_rate > 0
        # Taxa efetiva deve ser maior que a taxa nominal devido à capitalização composta
        assert result.summary.effective_annual_rate >= 0.12

    def test_final_balance_matches_last_monthly_balance(self, use_case: SimulateInvestmentUseCase):
        """Verifica se o saldo final corresponde ao último mês"""
        # Arrange
        investment = Investment(
            principal=2500.0,
            annual_rate=0.15,
            total_periods=18,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        last_month = result.monthly_evolution[-1]
        assert abs(result.summary.final_balance - last_month.final_balance) < 0.01

    def test_zero_principal_with_contributions(self, use_case: SimulateInvestmentUseCase):
        """Testa simulação com principal zero e apenas aportes"""
        # Arrange
        contribution = Contribution(
            amount=1000.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=0.0,
            annual_rate=0.12,
            total_periods=12,
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert result.summary.total_invested == 12000.0
        assert result.summary.total_deposits == 12000.0
        assert result.summary.final_balance > 12000.0
        assert result.summary.total_interest > 0

    def test_high_interest_rate_scenario(self, use_case: SimulateInvestmentUseCase):
        """Testa cenário com taxa de juros alta"""
        # Arrange
        investment = Investment(
            principal=1000.0,
            annual_rate=0.50,  # 50% ao ano
            total_periods=12,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert result.summary.final_balance > 1400.0
        assert result.summary.total_interest > 400.0

    def test_long_term_investment_60_months(self, use_case: SimulateInvestmentUseCase):
        """Testa investimento de longo prazo (5 anos)"""
        # Arrange
        contribution = Contribution(
            amount=300.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=5000.0,
            annual_rate=0.10,
            total_periods=60,  # 5 anos
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert len(result.monthly_evolution) == 60
        assert len(result.yearly_evolution) == 5
        assert result.summary.total_invested == 5000.0 + (300.0 * 60)
        assert result.summary.final_balance > result.summary.total_invested

        # Verifica progressão anual dos juros (deve aumentar a cada ano)
        for i in range(1, len(result.yearly_evolution)):
            assert result.yearly_evolution[i].interest_this_year > result.yearly_evolution[i-1].interest_this_year

    def test_deposits_total_accumulates_correctly(self, use_case: SimulateInvestmentUseCase):
        """Verifica se o total de depósitos acumula corretamente"""
        # Arrange
        contribution = Contribution(
            amount=150.0,
            frequency=CompoundingFrequency.MONTHLY
        )
        investment = Investment(
            principal=1000.0,
            annual_rate=0.12,
            total_periods=6,
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        expected_accumulated = 0.0
        for i, monthly in enumerate(result.monthly_evolution):
            expected_accumulated += 150.0
            assert monthly.deposits_total == expected_accumulated

    def test_return_type_is_full_simulation_report(self, use_case: SimulateInvestmentUseCase):
        """Verifica se o tipo de retorno é FullSimulationReport"""
        # Arrange
        investment = Investment(
            principal=1000.0,
            annual_rate=0.12,
            total_periods=12,
            compounding_frequency=CompoundingFrequency.MONTHLY
        )

        # Act
        result = use_case.execute(investment)

        # Assert
        assert isinstance(result, FullSimulationReport)
        assert isinstance(result.summary, SimulationSummary)
        assert all(isinstance(m, MonthlySummary) for m in result.monthly_evolution)
        assert all(isinstance(y, YearSummary) for y in result.yearly_evolution)


class TestSimulationComparativeAnalysis:
    """Testes de análise comparativa - imprimem relatórios detalhados no console"""

    @pytest.fixture
    def use_case(self) -> SimulateInvestmentUseCase:
        return SimulateInvestmentUseCase()

    def test_comparative_analysis_different_rates(self, use_case: SimulateInvestmentUseCase):
        """Análise comparativa: mesmo investimento com diferentes taxas de juros"""
        print("\n\n")
        print("🔍" * 40)
        print(" ANÁLISE COMPARATIVA: DIFERENTES TAXAS DE JUROS ".center(80, "🔍"))
        print("🔍" * 40)

        rates = [0.06, 0.10, 0.12, 0.15]  # 6%, 10%, 12%, 15%
        contribution = Contribution(amount=500.0, frequency=CompoundingFrequency.MONTHLY)

        for rate in rates:
            investment = Investment(
                principal=10000.0,
                annual_rate=rate,
                total_periods=60,  # 5 anos
                compounding_frequency=CompoundingFrequency.MONTHLY,
                contribution=contribution
            )
            result = use_case.execute(investment)
            print_simulation_report(result, f"TAXA ANUAL: {rate * 100:.0f}%")

        assert True

    def test_comparative_analysis_different_contributions(self, use_case: SimulateInvestmentUseCase):
        """Análise comparativa: mesmo investimento com diferentes aportes mensais"""
        print("\n\n")
        print("💰" * 40)
        print(" ANÁLISE COMPARATIVA: DIFERENTES APORTES MENSAIS ".center(80, "💰"))
        print("💰" * 40)

        contributions = [0.0, 200.0, 500.0, 1000.0]

        for amount in contributions:
            contribution = Contribution(amount=amount, frequency=CompoundingFrequency.MONTHLY) if amount > 0 else None
            investment = Investment(
                principal=10000.0,
                annual_rate=0.12,  # 12% ao ano
                total_periods=36,  # 3 anos
                compounding_frequency=CompoundingFrequency.MONTHLY,
                contribution=contribution
            )
            result = use_case.execute(investment)
            print_simulation_report(result, f"APORTE MENSAL: R$ {amount:,.2f}")

        assert True

    def test_comparative_analysis_different_periods(self, use_case: SimulateInvestmentUseCase):
        """Análise comparativa: mesmo investimento com diferentes períodos"""
        print("\n\n")
        print("📅" * 40)
        print(" ANÁLISE COMPARATIVA: DIFERENTES PERÍODOS DE INVESTIMENTO ".center(80, "📅"))
        print("📅" * 40)

        periods = [12, 24, 36, 60, 120]  # 1, 2, 3, 5, 10 anos
        contribution = Contribution(amount=300.0, frequency=CompoundingFrequency.MONTHLY)

        for period in periods:
            investment = Investment(
                principal=5000.0,
                annual_rate=0.10,  # 10% ao ano
                total_periods=period,
                compounding_frequency=CompoundingFrequency.MONTHLY,
                contribution=contribution
            )
            result = use_case.execute(investment)
            years = period // 12
            print_simulation_report(result, f"PERÍODO: {years} ANO(S) ({period} meses)")

        assert True

    def test_comparative_analysis_real_scenario(self, use_case: SimulateInvestmentUseCase):
        """Análise comparativa: cenários reais de investimento"""
        print("\n\n")
        print("🎯" * 40)
        print(" ANÁLISE COMPARATIVA: CENÁRIOS REAIS DE INVESTIMENTO ".center(80, "🎯"))
        print("🎯" * 40)

        scenarios = [
            {
                "name": "Conservador (Poupança ~6% a.a.)",
                "principal": 10000.0,
                "rate": 0.06,
                "contribution": 500.0,
                "periods": 60
            },
            {
                "name": "Moderado (CDB/LCI ~10% a.a.)",
                "principal": 10000.0,
                "rate": 0.10,
                "contribution": 500.0,
                "periods": 60
            },
            {
                "name": "Arrojado (Fundos/Ações ~15% a.a.)",
                "principal": 10000.0,
                "rate": 0.15,
                "contribution": 500.0,
                "periods": 60
            },
            {
                "name": "Aposentadoria (30 anos, 10% a.a.)",
                "principal": 20000.0,
                "rate": 0.10,
                "contribution": 1000.0,
                "periods": 360
            },
        ]

        for scenario in scenarios:
            contribution = Contribution(
                amount=scenario["contribution"],
                frequency=CompoundingFrequency.MONTHLY
            )
            investment = Investment(
                principal=scenario["principal"],
                annual_rate=scenario["rate"],
                total_periods=scenario["periods"],
                compounding_frequency=CompoundingFrequency.MONTHLY,
                contribution=contribution
            )
            result = use_case.execute(investment)
            print_simulation_report(result, scenario["name"].upper())

        assert True

    def test_validation_scenario_6pct_6000_monthly_6years(self, use_case: SimulateInvestmentUseCase):
        """
        Cenário para validação com outro aplicativo:
        - Taxa anual: 6%
        - Saldo inicial: R$ 0,00
        - Depósito mensal: R$ 6.000,00
        - Período: 6 anos (72 meses)
        """
        print("\n\n")
        print("✅" * 40)
        print(" CENÁRIO DE VALIDAÇÃO - COMPARAR COM OUTRO APLICATIVO ".center(80, "✅"))
        print("✅" * 40)
        print("\n📋 PARÂMETROS DO CENÁRIO:")
        print("-" * 40)
        print("  • Taxa anual:        6%")
        print("  • Saldo inicial:     R$ 0,00")
        print("  • Depósito mensal:   R$ 6.000,00")
        print("  • Período:           6 anos (72 meses)")
        print("-" * 40)

        contribution = Contribution(amount=6000.0, frequency=CompoundingFrequency.MONTHLY)
        investment = Investment(
            principal=0.0,
            annual_rate=0.06,  # 6% ao ano
            total_periods=72,  # 6 anos
            compounding_frequency=CompoundingFrequency.MONTHLY,
            contribution=contribution
        )
        result = use_case.execute(investment)
        print_simulation_report(result, "VALIDAÇÃO: 6% a.a. | R$ 0 inicial | R$ 6.000/mês | 6 anos")

        # Dados esperados para validação
        print("\n📊 DADOS PARA VALIDAÇÃO:")
        print("-" * 60)
        print(f"  • Total Investido:     R$ {result.summary.total_invested:,.2f}")
        print(f"  • Total de Juros:      R$ {result.summary.total_interest:,.2f}")
        print(f"  • Saldo Final:         R$ {result.summary.final_balance:,.2f}")
        print(f"  • Taxa Mensal:         {0.06/12 * 100:.6f}%")
        print(f"  • Taxa Efetiva Anual:  {result.summary.effective_annual_rate * 100:.4f}%")
        print("-" * 60)

        # Assertions básicas
        assert result.summary.total_invested == 6000.0 * 72  # R$ 432.000,00
        assert result.summary.total_deposits == 6000.0 * 72
        assert result.summary.final_balance > result.summary.total_invested
        assert len(result.monthly_evolution) == 72
        assert len(result.yearly_evolution) == 6

    def test_summary_comparison_table(self, use_case: SimulateInvestmentUseCase):
        """Gera uma tabela resumida para comparação rápida de cenários"""
        print("\n\n")
        print("=" * 120)
        print(" 📊 TABELA COMPARATIVA DE CENÁRIOS DE INVESTIMENTO 📊 ".center(120, "="))
        print("=" * 120)

        scenarios = [
            ("Poupança 5 anos", 10000.0, 0.06, 500.0, 60),
            ("CDB 5 anos", 10000.0, 0.10, 500.0, 60),
            ("Fundos 5 anos", 10000.0, 0.15, 500.0, 60),
            ("CDB 10 anos", 10000.0, 0.10, 500.0, 120),
            ("Aposentadoria 30 anos", 20000.0, 0.10, 1000.0, 360),
        ]

        print(f"\n{'Cenário':<25}{'Principal':>15}{'Aporte':>12}{'Taxa':>8}{'Período':>10}"
              f"{'Total Invest.':>18}{'Saldo Final':>18}{'Juros':>18}{'Rend.%':>10}")
        print("-" * 134)

        for name, principal, rate, contribution_amount, periods in scenarios:
            contribution = Contribution(amount=contribution_amount, frequency=CompoundingFrequency.MONTHLY)
            investment = Investment(
                principal=principal,
                annual_rate=rate,
                total_periods=periods,
                compounding_frequency=CompoundingFrequency.MONTHLY,
                contribution=contribution
            )
            result = use_case.execute(investment)

            rendimento = (result.summary.total_interest / result.summary.total_invested) * 100
            years = periods // 12

            print(f"{name:<25}{principal:>15,.2f}{contribution_amount:>12,.2f}{rate*100:>7.1f}%{years:>8} anos"
                  f"{result.summary.total_invested:>18,.2f}{result.summary.final_balance:>18,.2f}"
                  f"{result.summary.total_interest:>18,.2f}{rendimento:>9.1f}%")

        print("=" * 134)
        print("\n")

        assert True

