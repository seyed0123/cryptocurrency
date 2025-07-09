// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title ERC-20 Token representing stock shares
contract StockToken is ERC20 {
    address public market;

    modifier onlyMarket() {
        require(msg.sender == market, "Only StockMarket can call");
        _;
    }

    constructor(string memory name, string memory symbol, address _market) ERC20(name, symbol) {
        market = _market;
    }

    function mint(address to, uint256 amount) external onlyMarket {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyMarket {
        _burn(from, amount);
    }
}