// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "contracts/StockToken.sol";

/// @title Stock Market contract acting as a factory and controller
contract StockMarket is Ownable {
    struct Stock {
        string name;
        address token;
        uint256 lastPrice; // scaled price, e.g., with 8 decimals
        uint256 lastUpdated;
    }

    mapping(string => Stock) public stocks; // symbol => Stock
    mapping(string => bool) public registered;

    event StockAdded(string symbol, address tokenAddress);
    event PriceUpdated(string symbol, uint256 price, uint256 timestamp);

    constructor() Ownable(msg.sender) {}

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
