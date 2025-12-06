"""
Return on Equity (ROE) Calculator for Multifamily Properties
Conservative underwriting: 0% appreciation assumption
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from src.utils import get_logger

logger = get_logger(__name__)


# ROE Tier Definitions
ROE_TIERS = {
    'unicorn': {'min': 0.20, 'color': 'purple', 'icon': 'star', 'label': '🦄 UNICORN'},
    'strong': {'min': 0.15, 'color': 'green', 'icon': 'home', 'label': '🟢 Strong Buy'},
    'marginal': {'min': 0.10, 'color': 'orange', 'icon': 'info-sign', 'label': '🟡 Marginal'},
    'pass': {'min': 0.00, 'color': 'red', 'icon': 'remove', 'label': '🔴 Pass'}
}


class ROECalculator:
    """
    Calculate Year 1 Return on Equity for multifamily properties
    Uses conservative assumptions (0% appreciation)
    """
    
    def __init__(
        self,
        operating_expense_ratio: float = 0.35,
        down_payment_pct: float = 0.25,
        interest_rate: float = 0.07,
        loan_term_years: int = 30,
        appreciation_rate: float = 0.0  # Conservative default
    ):
        """
        Initialize ROE calculator with default assumptions
        
        Args:
            operating_expense_ratio: Operating expenses as % of gross income (default 35%)
            down_payment_pct: Down payment as % of purchase price (default 25%)
            interest_rate: Annual interest rate (default 7%)
            loan_term_years: Loan term in years (default 30)
            appreciation_rate: Annual appreciation rate (default 0% - conservative)
        """
        self.opex_ratio = operating_expense_ratio
        self.down_pct = down_payment_pct
        self.rate = interest_rate
        self.term = loan_term_years
        self.appreciation = appreciation_rate
        
        logger.info(
            f"ROECalculator initialized: {self.opex_ratio:.0%} OpEx, "
            f"{self.down_pct:.0%} down, {self.rate:.1%} rate, "
            f"{self.appreciation:.1%} appreciation"
        )
    
    def estimate_market_rent(self, zip_code: str, sqft_per_unit: float) -> float:
        """
        Estimate market rent per unit based on location and size
        
        Args:
            zip_code: Property ZIP code
            sqft_per_unit: Average sqft per unit
            
        Returns:
            Estimated monthly rent per unit
        """
        # Base rent by ZIP (simplified - could be expanded with real market data)
        # Dallas urban core: higher rents
        high_rent_zips = ['75201', '75204', '75205', '75219', '75225', '76107', '76109']
        # Mid-tier
        mid_rent_zips = ['75206', '75214', '75218', '75223', '75235', '76102', '76104', '76105']
        # Value areas
        # Everything else is value
        
        if zip_code in high_rent_zips:
            base_rate = 1.40  # $1.40/sqft
        elif zip_code in mid_rent_zips:
            base_rate = 1.20  # $1.20/sqft
        else:
            base_rate = 1.00  # $1.00/sqft
        
        # Calculate rent based on sqft
        monthly_rent = sqft_per_unit * base_rate
        
        # Floor and ceiling (reasonableness check)
        monthly_rent = max(800, min(monthly_rent, 2500))
        
        return monthly_rent
    
    def calculate_mortgage_payment(
        self,
        loan_amount: float,
        annual_rate: float,
        years: int
    ) -> float:
        """
        Calculate monthly mortgage payment
        
        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate (e.g., 0.07 for 7%)
            years: Loan term in years
            
        Returns:
            Monthly payment amount
        """
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / (
            (1 + monthly_rate) ** num_payments - 1
        )
        
        return payment
    
    def calculate_principal_paydown_year1(
        self,
        loan_amount: float,
        monthly_payment: float,
        annual_rate: float
    ) -> float:
        """
        Calculate total principal paid down in Year 1
        
        Args:
            loan_amount: Initial loan amount
            monthly_payment: Monthly payment
            annual_rate: Annual interest rate
            
        Returns:
            Total principal paid in first year
        """
        monthly_rate = annual_rate / 12
        balance = loan_amount
        total_principal = 0
        
        # Calculate for 12 months
        for _ in range(12):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            total_principal += principal_payment
            balance -= principal_payment
        
        return total_principal
    
    def calculate_roe(
        self,
        purchase_price: float,
        units: int,
        sqft: float,
        zip_code: str,
        monthly_rent_per_unit: Optional[float] = None
    ) -> Dict:
        """
        Calculate Year 1 ROE for a property
        
        Args:
            purchase_price: Property purchase price
            units: Number of units
            sqft: Total square footage
            zip_code: ZIP code for rent estimation
            monthly_rent_per_unit: Actual rent (if known), otherwise estimated
            
        Returns:
            Dictionary with all ROE calculations
        """
        # Estimate rent if not provided
        if monthly_rent_per_unit is None:
            sqft_per_unit = sqft / units if sqft and units else 1000
            monthly_rent_per_unit = self.estimate_market_rent(zip_code, sqft_per_unit)
        
        # Annual gross rent
        annual_gross_rent = monthly_rent_per_unit * units * 12
        
        # Operating expenses
        annual_opex = annual_gross_rent * self.opex_ratio
        
        # Net Operating Income
        noi = annual_gross_rent - annual_opex
        
        # Financing
        down_payment = purchase_price * self.down_pct
        loan_amount = purchase_price - down_payment
        
        # Debt service
        monthly_payment = self.calculate_mortgage_payment(
            loan_amount, self.rate, self.term
        )
        annual_debt_service = monthly_payment * 12
        
        # Cash flow
        cash_flow = noi - annual_debt_service
        
        # Principal paydown (Year 1)
        principal_year1 = self.calculate_principal_paydown_year1(
            loan_amount, monthly_payment, self.rate
        )
        
        # Appreciation (default 0%)
        appreciation_value = purchase_price * self.appreciation
        
        # Total return
        total_return = cash_flow + principal_year1 + appreciation_value
        
        # ROE
        roe = total_return / down_payment if down_payment > 0 else 0
        
        # Cash-on-cash
        coc = cash_flow / down_payment if down_payment > 0 else 0
        
        # Cap rate
        cap_rate = noi / purchase_price if purchase_price > 0 else 0
        
        return {
            # Inputs
            'purchase_price': purchase_price,
            'units': units,
            'monthly_rent_per_unit': monthly_rent_per_unit,
            'zip_code': zip_code,
            
            # Financing
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            
            # Income
            'annual_gross_rent': annual_gross_rent,
            'annual_opex': annual_opex,
            'opex_ratio': self.opex_ratio,
            'noi': noi,
            
            # Returns
            'annual_debt_service': annual_debt_service,
            'cash_flow': cash_flow,
            'principal_paydown': principal_year1,
            'appreciation': appreciation_value,
            'total_return': total_return,
            
            # Metrics
            'roe': roe,
            'coc': coc,
            'cap_rate': cap_rate,
            'meets_hurdle': roe >= 0.15,
            'tier': get_roe_tier(roe)
        }
    
    def analyze_portfolio(self, properties_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate ROE for all properties in a DataFrame
        
        Args:
            properties_df: DataFrame with columns: price, units, sqft, zip_code
            
        Returns:
            DataFrame with ROE calculations added
        """
        logger.info(f"Analyzing {len(properties_df)} properties...")
        
        results = []
        
        for idx, row in properties_df.iterrows():
            try:
                roe_calc = self.calculate_roe(
                    purchase_price=row['price'],
                    units=row['units'],
                    sqft=row.get('sqft', None),
                    zip_code=row['zip_code']
                )
                
                # Combine original row with calculations
                result = {**row.to_dict(), **roe_calc}
                results.append(result)
                
            except Exception as e:
                logger.warning(f"Failed to calculate ROE for {row.get('address', 'unknown')}: {e}")
                continue
        
        result_df = pd.DataFrame(results)
        
        # Summary stats
        unicorns = len(result_df[result_df['roe'] >= 0.20])
        strong = len(result_df[(result_df['roe'] >= 0.15) & (result_df['roe'] < 0.20)])
        marginal = len(result_df[(result_df['roe'] >= 0.10) & (result_df['roe'] < 0.15)])
        
        logger.info(
            f"ROE Analysis Complete: "
            f"{unicorns} unicorns (20%+), "
            f"{strong} strong (15-20%), "
            f"{marginal} marginal (10-15%)"
        )
        
        return result_df


def get_roe_tier(roe: float) -> dict:
    """
    Get the ROE tier info for a given ROE value
    
    Args:
        roe: Return on Equity as decimal (e.g., 0.15 for 15%)
        
    Returns:
        Tier dictionary with color, icon, label
    """
    if roe >= 0.20:
        return ROE_TIERS['unicorn']
    elif roe >= 0.15:
        return ROE_TIERS['strong']
    elif roe >= 0.10:
        return ROE_TIERS['marginal']
    else:
        return ROE_TIERS['pass']


def format_roe_summary(roe_data: Dict) -> str:
    """
    Format ROE calculation as human-readable summary
    
    Args:
        roe_data: Dictionary from calculate_roe()
        
    Returns:
        Formatted string
    """
    tier = roe_data['tier']
    
    summary = f"""
{'='*60}
{tier['label']} - ROE: {roe_data['roe']:.1%}
{'='*60}

Investment:
  Purchase Price:        ${roe_data['purchase_price']:,.0f}
  Down Payment (25%):    ${roe_data['down_payment']:,.0f}
  Loan (75% @ 7%, 30yr): ${roe_data['loan_amount']:,.0f}

Property:
  Units:                 {roe_data['units']:.0f}
  Est. Rent/Unit:        ${roe_data['monthly_rent_per_unit']:,.0f}/mo

Income:
  Gross Rents:           ${roe_data['annual_gross_rent']:,.0f}/yr
  Operating Expenses:   -${roe_data['annual_opex']:,.0f}/yr ({roe_data['opex_ratio']:.0%})
  Net Operating Income:  ${roe_data['noi']:,.0f}/yr

Cash Flow:
  NOI:                   ${roe_data['noi']:,.0f}
  Debt Service:         -${roe_data['annual_debt_service']:,.0f}
  Annual Cash Flow:      ${roe_data['cash_flow']:,.0f} ({roe_data['coc']:.1%} CoC)

Year 1 Wealth Creation:
  💵 Cash Flow:          ${roe_data['cash_flow']:,.0f}
  🏦 Principal Paydown:  ${roe_data['principal_paydown']:,.0f}
  📈 Appreciation:       ${roe_data['appreciation']:,.0f} (0% assumption)
  {'─'*60}
  💰 Total Return:       ${roe_data['total_return']:,.0f}

🎯 RETURN ON EQUITY: {roe_data['roe']:.1%}
   Cap Rate: {roe_data['cap_rate']:.2%}
{'='*60}
"""
    return summary