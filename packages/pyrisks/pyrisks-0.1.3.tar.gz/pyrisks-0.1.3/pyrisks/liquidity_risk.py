import pandas as pd
import numpy as np

# Este es un comentario
class LiquidityRisk:
    """LiquidityRisk contains functions used for measuring the liquidity risk 
    exposure given the portfolio of assets, those assets haircuts and the 
    transactions carried."""
    
    def HQLA(Portfolio: pd.DataFrame, Haircuts: pd.DataFrame, 
            Portfolio_columns: dict, Haircuts_columns: dict) -> float:
        """
        Calculate the value of the High Quality Liquid Assets in the portfolio.
        Which consist in applying a haircut to every asset in the portfolio
        depending on it's level of liquidity and adding the total discounted
        value of the assets. The haircut represents how much of the asset's
        value may be loss when selling it in a short time, assets with lower 
        liquidity tend to receive higher punishment when selling them in short
        time..
        
        Parameters
        ----------
        Portfolio : pd.DataFrame
            DataFrame containing all assets in the portfolio, which may include
            bonds, stocks and cash. the DataFrame must contain an ID column with
            a unique identifier for every asset (i.e. ISIN) and a market value
            column with the value for which the asset may be sold in the market. 
            It should only include cash and any assets that are available to be 
            sold.
        Haircuts : pd.DataFrame
            DataFrame containing the haircut that correspond to every asset in
            the portfolio. the DataFrame must contain an ID column with a unique 
            identifier for every asset (i.e. ISIN) and a haircut column with the
            corresponding haircut for every asset. If a haircut isn't provided
            for an asset in the portfolio, the function will assign a haircut of
            100%, meaning that it won't be taken into account in the HQLA.
        Portfolio_columns : dict
            Dictionary with the names of the columns containing asset ID and 
            market value in the portfolio DataFrame. The dictionary keys must
            be {"Asset_ID": "", "Market_Value": ""}.
        Haircuts_columns : dict, optional
            Dictionary with the names of the columns containing asset ID and 
            haircut in the haircuts DataFrame. The dictionary keys must be 
            {"Asset_ID": "", "haircut": ""}.

        Returns
        -------
        float
            Total value of High Quality Liquid Assets, which is the sum of 
            assets' market value discounting a haircut for the losses that may 
            be done when selling the asset in a short time.

        """
        
        # Map each haircut to its corresponding asset
        Portfolio["Haircut"] = Portfolio[Portfolio_columns["Asset_ID"]].map(
            dict(zip(Haircuts[Haircuts_columns["Asset_ID"]], 
                     Haircuts[Haircuts_columns["haircut"]])))
        Portfolio["Haircut"] = Portfolio["Haircut"].fillna(1)
        
        # Calculate the value of assets discounting haircut
        Portfolio["MARKET_VALUE_HC"] = \
        Portfolio[Portfolio_columns["Market_Value"]]*(1-Portfolio["Haircut"])
        
        # HQLA is the sum of asset values discounting haircuts
        HQLA = Portfolio["MARKET_VALUE_HC"].sum()
        
        return HQLA
        
        
    def Requirements(transactions: pd.DataFrame, 
            haircuts: pd.DataFrame, transactions_columns: dict, 
            haircuts_columns: dict) -> float:
        """
        Calculate the value of liquidity requirements for sustaining transactions. 
        Liquidity requirements measure the amount of liquid assets needed for 
        supporting intermediation activities where an asset is bought or sold 
        from a third party. In this scenario, liquid assets are required in case 
        any of the parties fail to complete their part of the deal and an asset 
        must be bought or sold in a short time with posible losses depending on 
        the liquidity of the asset. This is calculated by taking the positive 
        and negative flows of each transaction. The positive flow of the buy 
        transaction gets a haircut as it is the asset bought and is susceptible
        to losses in case the buying party doesn't bring the money and the asset 
        needs to be sold in the market in short time. The difference between 
        negative flows and positive flows is the Liquidity Requirements as it 
        represents the losses that can be done in these transactions.

        Parameters
        ----------
        transactions : pd.DataFrame
            Dataframe must include all transactions executed by own position 
            and third parties that are still pending settlement, thus 
            recognizing them as future liquidity requirements. The structure 
            includes the following columns:
                - 'asset_id': unique identifier for each security involved in 
                    the transaction performed (i.e. ISIN). 
                - 'transaction_type': classification of the type of transaction 
                    performed. Whether it's a purchase (Buy:B) or a sale (Sell:S).
                - 'current_valuation': current valuation of the corresponding 
                    asset in the transaction. 
                - 'transaction_value': value at which the transaction was agreed 
                    upon.
        haircuts : pd.DataFrame
            DataFrame containing the haircut that correspond to every asset in
            the portfolio. the DataFrame must contain an ID column with a unique 
            identifier for every asset (i.e. ISIN) and a haircut column with the
            corresponding haircut for every asset. If a haircut isn't provided
            for an asset in the portfolio, the function will assign a haircut of
            100%, meaning that it won't be taken into account in the liquidity
            requirements.
        transactions_columns : dict
            Dictionary with the names of the columns containing in the transactions 
            DataFrame. The dictionary keys must be {"asset_id": "",
                                                    "transaction_type": "",
                                                    "current_valuation": "",
                                                    "transaction_value": ""}.
        haircuts_columns : dict
            Dictionary with the names of the columns containing asset ID and 
            haircut in the haircuts DataFrame. The dictionary keys must be 
            {"asset_id": "", "haircut": ""}.


        Returns
        -------
        float
            The value of liquidity requirements corresponding to the indicated 
            transactions.

        """
        
        # Map each haircut to its corresponding transaction
        transactions["haircut"] = transactions[transactions_columns["asset_id"]].map(
            dict(zip(haircuts[haircuts_columns["asset_id"]], 
                     haircuts[haircuts_columns["haircut"]])))
        transactions["haircut"] = transactions["haircut"].fillna(1)
        
        # Adjustment of the valuation of the cash flows
        transactions['adjusted_valuation'] = \
            transactions[transactions_columns["current_valuation"]] * \
                (1 - transactions["haircut"])
        
        # Positive Cash Flows 
        transactions['positive_cf'] = \
            np.where(transactions[transactions_columns["transaction_type"]] == "B",
                     transactions['adjusted_valuation'],
                     transactions[transactions_columns["transaction_value"]])
    
        # Negative Cash Flows
        transactions['negative_cf'] = \
            np.where(transactions[transactions_columns["transaction_type"]] == "B",
                     transactions[transactions_columns["transaction_value"]],
                     transactions[transactions_columns["current_valuation"]])
    
        # Calculate liquidity requirements
        liquidity_requirements = transactions['negative_cf'].sum() - \
                            transactions['positive_cf'].sum()
        
        return liquidity_requirements
    
    
    def LR_indicator(liquidity_requirements:float, 
                     HQLA:float,
                     decimal_places = 4) -> float: 
        '''
        The 'LR_indicator' is the Liquidity Risk Indicator (LRI), which aims 
        to reflect the extent to which High-Quality Liquid Assets (HQLA) 
        adjusted for market risk and income cover the projected outflows by 
        the organization ('liquidity_requirements').

        Parameters
        ----------
        liquidity_requirements : float
            Value of liquidity requirements for sustaining transactions. 
            Liquidity requirements measure the amount of liquid assets needed for 
            supporting intermediation activities where an asset is bought or sold 
            from a third party. In this scenario, liquid assets are required in case 
            any of the parties fail to complete their part of the deal and an asset 
            must be bought or sold in a short time with posible losses depending on 
            the liquidity of the asset. 
        HQLA : float
            Value of the High Quality Liquid Assets in the portfolio.
            Which consist in applying a haircut to every asset in the portfolio
            depending on it's level of liquidity and adding the total discounted
            value of the assets.
        decimal_places : int 
            Number of decimal places desired for the indicator result. 
            Default is set to 4.

        Returns
        -------
        float
            The LRI measures the number of times the organization's high-quality 
            assets cover the amount or value of liquidity requirements derived 
            from its intermediation activities in financial market operations.

        '''
        
        return round(HQLA/liquidity_requirements , decimal_places)


        def TRequirements(transactions: pd.DataFrame, 
            haircuts: pd.DataFrame, transactions_columns: dict, 
            haircuts_columns: dict) -> float:

            # Map each haircut to its corresponding transaction
                
            transactions["haircut"] = transactions[transactions_columns["asset_id"]].map(
                dict(zip(haircuts[haircuts_columns["asset_id"]], 
                         haircuts[haircuts_columns["haircut"]])))
            transactions["haircut"] = transactions["haircut"].fillna(1)

            # Keep only selling transactions

            transactions = transactions.loc[transactions["transaction_type"]=='S', :]
            
            # Adjustment of the valuation of cash flows
    
            transactions["Adjusted_Valuation"] =  transactions["current_valuation"]*transactions["haircut"]

            TLiquidity_requirements = transactions["Ajusted_Valuation"].sum()
            
            return TLiquidity_requirements
                    



