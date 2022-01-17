"""
This is an APY Viewset for cruize smart contract.
This will have apis that compute and work around generating APR/APY for any asset.

"""

# Create your views here.
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from utilities import TokenUtilities
from apy.api.TokenAPYSerializer import TokenAPYSerializer


class TokenAPYViewset(GenericViewSet):
    def list(self, request):
        request_body = request.query_params
        self.serializer_class = TokenAPYSerializer
        serializer = self.serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        token_ticker = validated_data["token_ticker"]  # 'USDC'
        reward_token_ticker = validated_data["reward_token_ticker"]  # 'WETH'

        RAY = 10.0 ** 27
        WAD = 10.0 ** 18
        SECONDS_PER_YEAR = 31556926.0  # Number of seconds in a year. Required for token emission calculation

        URL_API = "https://api.thegraph.com/subgraphs/name/aave/aave-v2-matic"
        # URL_API = "https://gateway.thegraph.com/api/45e610b7b8c2623d2ed8cbb3912e822c/subgraphs/id/0x5ca1ea5549e4e7cb64ae35225e11865d2572b3f9-1"
        query = gql(
            """
        query {
          reserves (where: {
            usageAsCollateralEnabled: true
          }) {
            id
            name
            price {
              id
              priceInEth
            }
            liquidityRate
            variableBorrowRate
            stableBorrowRate
            aEmissionPerSecond
            vEmissionPerSecond
            decimals
            totalATokenSupply
            totalCurrentVariableDebt
            symbol
          }
        }
        """
        )

        sample_transport = RequestsHTTPTransport(
            url=URL_API,
            verify=True,
            retries=3,
        )
        client = Client(transport=sample_transport)

        response = client.execute(query)

        for token in response["reserves"]:
            if token_ticker in token["symbol"]:
                variableBorrowRate = float(token["variableBorrowRate"])
                liquidityRate = float(token["liquidityRate"])
                TOKEN_DECIMALS = 10 ** float(token["decimals"])
                aEmissionPerSecond = float(token["aEmissionPerSecond"])
                vEmissionPerSecond = float(token["vEmissionPerSecond"])
                totalCurrentVariableDebt = float(token["totalCurrentVariableDebt"])
                totalATokenSupply = float(token["totalATokenSupply"])
            if reward_token_ticker in token["symbol"]:
                REWARD_DECIMALS = 10 ** float(token["decimals"])

        REWARD_PRICE_ETH = TokenUtilities.get_token_price_in_eth(reward_token_ticker)
        TOKEN_PRICE_ETH = TokenUtilities.get_token_price_in_eth(
            token_ticker.replace("W", "")
        )

        # deposit and borrow calculation

        percentDepositAPY = 100.0 * liquidityRate / RAY
        percentVariableBorrowAPY = 100.0 * variableBorrowRate / RAY
        percentStableBorrowAPY = 100.0 * variableBorrowRate / RAY

        print(
            f"{token_ticker} deposit APY: {percentDepositAPY:.2f}%"
        )  # Will replace with a logger once we have data visualization
        print(
            f"{token_ticker} borrow APY: {percentVariableBorrowAPY:.2f}%"
        )  # Will replace with a logger once we have data visualization

        percentDepositAPR = (
            100
            * (
                aEmissionPerSecond
                * SECONDS_PER_YEAR
                * REWARD_PRICE_ETH
                * TOKEN_DECIMALS
            )
            / (totalATokenSupply * TOKEN_PRICE_ETH * REWARD_DECIMALS)
        )
        percentBorrowAPR = (
            100
            * (
                vEmissionPerSecond
                * SECONDS_PER_YEAR
                * REWARD_PRICE_ETH
                * TOKEN_DECIMALS
            )
            / (totalCurrentVariableDebt * TOKEN_PRICE_ETH * REWARD_DECIMALS)
        )

        print(
            f"{token_ticker} WETH reward deposit APR: {percentDepositAPR:.2f}%"
        )  # Will replace with a logger once we have data visualization
        print(
            f"{token_ticker} WETH reward borrow APR: {percentBorrowAPR:.2f}%"
        )  # Will replace with a logger once we have data visualization
        response_data = {
            reward_token_ticker: {
                "APR": f"{percentDepositAPR:.2f}%",
                "APY": f"{percentBorrowAPR:.2f}%",
            }
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
