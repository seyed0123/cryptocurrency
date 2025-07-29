// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import {Chainlink, ChainlinkClient} from "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "contracts/StockToken.sol";

/// @title Stock Market contract acting as a factory and controller
contract StockMarket is Ownable, ChainlinkClient {
    using Chainlink for Chainlink.Request;
    struct Stock {
        string name;
        address token;
        uint256 lastPrice; // scaled price, e.g., with 8 decimals
        uint256 lastUpdated;
    }

    mapping(string => Stock) public stocks; // symbol => Stock
    mapping(string => bool) public registered;
    mapping(bytes32 => string) public requestIdToSymbol;
    address public oracle;
    bytes32 public jobId;
    uint256 private constant ORACLE_PAYMENT = (1 * LINK_DIVISIBILITY) / 10;
    


    event StockAdded(string symbol, address tokenAddress);
    event PriceUpdated(string symbol, uint256 price, uint256 timestamp);

    constructor(string memory jobId_, address oracle_) Ownable(msg.sender) {
        _setChainlinkToken(0x779877A7B0D9E8603169DdbD7836e478b4624789);

        jobId = stringToBytes32(jobId_);
        oracle = oracle_;
    }

    function stringToBytes32(
        string memory source
    ) private pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            // solhint-disable-line no-inline-assembly
            result := mload(add(source, 32))
        }
    }

    /// @notice Add a new stock and deploy its ERC20 token
    function addStock(string calldata symbol, string calldata name) external onlyOwner {
        require(!registered[symbol], "Stock already registered");

        StockToken token = new StockToken(name, symbol, address(this));
        stocks[symbol] = Stock({
            name: name,
            token: address(token),
            lastPrice: 0,
            lastUpdated: 0
        });

        registered[symbol] = true;
        emit StockAdded(symbol, address(token));
    }

    function requestPriceUpdate(string memory symbol) public onlyOwner returns (bytes32 requestId) {
        require(registered[symbol], "Stock not registered");

        string memory url = string(
            abi.encodePacked(
                "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=",
                symbol,
                "&apikey=9EYH50S2XRUVP7HM"
            )
        );

        Chainlink.Request memory req = _buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfillPrice.selector
        );

        req._add("get", url);
        req._add("path", "Global Quote.05. price");

        requestId = _sendChainlinkRequestTo(oracle, req, ORACLE_PAYMENT);

        requestIdToSymbol[requestId] = symbol;
    }

    /// @notice Callback function for Chainlink oracle to fulfill price data
    function fulfillPrice(
        bytes32 _requestId,
        uint256 _price
    ) public recordChainlinkFulfillment(_requestId) {
        string memory symbol = requestIdToSymbol[_requestId];
        require(registered[symbol], "Invalid symbol in fulfillment");

        stocks[symbol].lastPrice = _price;
        stocks[symbol].lastUpdated = block.timestamp;

        emit PriceUpdated(symbol, _price, block.timestamp);
    }



    /// @notice Update price manually (placeholder, to be replaced with Chainlink integration)
    function updatePrice(string calldata symbol, uint256 newPrice) external onlyOwner {
        require(registered[symbol], "Stock not found");
        stocks[symbol].lastPrice = newPrice;
        stocks[symbol].lastUpdated = block.timestamp;
        emit PriceUpdated(symbol, newPrice, block.timestamp);
    }

    /// @notice Buy shares using ETH (example logic, no actual pricing calc)
    function buyStock(string calldata symbol, uint256 amount) external payable {
        require(registered[symbol], "Invalid stock");

        Stock storage stock = stocks[symbol];
        require(block.timestamp - stock.lastUpdated < 1 hours, "Stale price");

        uint256 cost = (stock.lastPrice * amount) / 1e8;
        require(msg.value >= cost, "Insufficient payment");

        StockToken token = StockToken(stock.token);
        token.mint(msg.sender, amount);
    }

    /// @notice Sell shares back (burn token, refund ETH for example)
    function sellStock(string calldata symbol, uint256 amount) external {
        require(registered[symbol], "Invalid stock");

        Stock storage stock = stocks[symbol];
        require(block.timestamp - stock.lastUpdated < 1 hours, "Stale price");

        uint256 payout = (stock.lastPrice * amount) / 1e8;
        require(address(this).balance >= payout, "Contract lacks funds");

        StockToken token = StockToken(stock.token);
        token.burn(msg.sender, amount);
        payable(msg.sender).transfer(payout);
    }

    /// @notice Fallback to receive ETH
    receive() external payable {}
}