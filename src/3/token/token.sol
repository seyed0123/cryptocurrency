// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IERC20.sol";
  /**
   * @title soltantocken
   * @dev ContractDescription
   * @custom:dev-run-script token.sol
   */
contract Solancoin is IERC20{
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public override totalSupply;
    bool public pause;

    address public deployer;
    uint256 public maxSupply;
    uint256 public deploymentBlock;
    uint256 public blockLockLimit = 0;

    mapping(address => uint256) public override balanceOf;
    mapping(address => mapping(address => uint256)) public override allowance;
    mapping(address => bool) public whitelist;

    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);

    modifier onlyDeployer() {
        require(msg.sender == deployer, "Only deployer allowed");
        _;
    }

    modifier canTransfer(address sender) {
        if (pause || block.number < deploymentBlock + blockLockLimit) {
            require(
            msg.sender == deployer || whitelist[msg.sender],
            "Transfer locked for non-whitelisted addresses"
        );
        }
        _;
    }

    constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        deployer = msg.sender;
        deploymentBlock = block.number;
        pause = false;

        uint256 initial = _initialSupply * (10 ** uint256(decimals));
        totalSupply = initial;
        balanceOf[deployer] = initial;
        maxSupply = initial * 5;

        emit Transfer(address(0), deployer, initial);
    }

    function transfer(address recipient, uint256 amount) public override canTransfer(msg.sender) returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public override returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public override canTransfer(sender) returns (bool) {
        require(balanceOf[sender] >= amount, "Insufficient balance");
        require(allowance[sender][msg.sender] >= amount, "Allowance exceeded");

        balanceOf[sender] -= amount;
        balanceOf[recipient] += amount;
        allowance[sender][msg.sender] -= amount;

        emit Transfer(sender, recipient, amount);
        return true;
    }

    function setBlockLockLimit(uint256 newLimit) public onlyDeployer {
        blockLockLimit = newLimit;
    }

    function setPause(bool newPause) public onlyDeployer{
        pause = newPause;
    } 

    function addToWhitelist(address _addr) external onlyDeployer {
    whitelist[_addr] = true;
    }

    function removeFromWhitelist(address _addr) external onlyDeployer {
        whitelist[_addr] = false;
    }

    function mint(uint256 amount) public onlyDeployer {
        require(block.number <= deploymentBlock + 10000, "Minting period expired");
        uint256 newSupply = totalSupply + amount;
        require(newSupply <= maxSupply, "Exceeds max supply");

        balanceOf[deployer] += amount;
        totalSupply = newSupply;

        emit Mint(deployer, amount);
        emit Transfer(address(0), deployer, amount);
    }

    function burn(uint256 amount) public {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance to burn");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;

        emit Burn(msg.sender, amount);
        emit Transfer(msg.sender, address(0), amount);
    }
}
