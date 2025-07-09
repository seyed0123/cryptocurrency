// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract Oracle {
    address public owner;
    mapping(bytes32 => bool) public pendingRequests;
    event OracleRequest(
        bytes32 indexed specId,
        address requester,
        bytes32 requestId,
        uint256 payment,
        address callbackAddr,
        bytes4 callbackFunctionId,
        uint256 cancelExpiration,
        uint256 dataVersion,
        bytes data
    );

    event OracleResponse(bytes32 indexed requestId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function oracleRequest(
        address sender,
        uint256 payment,
        bytes32 specId,
        address callbackAddr,
        bytes4 callbackFunctionId,
        uint256 nonce,
        uint256 dataVersion,
        bytes calldata data
    ) external returns (bytes32 requestId) {
        requestId = keccak256(abi.encodePacked(sender, nonce));
        pendingRequests[requestId] = true;

        emit OracleRequest(
            specId,
            sender,
            requestId,
            payment,
            callbackAddr,
            callbackFunctionId,
            block.timestamp + 5 minutes,
            dataVersion,
            data
        );
    }

    function fulfillOracleRequest(
        bytes32 requestId,
        // uint256 payment,
        address callbackAddr,
        bytes4 callbackFunctionId,
        // uint256 expiration,
        bytes calldata data
    ) external onlyOwner returns (bool) {
        require(pendingRequests[requestId], "Request not found");
        delete pendingRequests[requestId];

        (bool success, ) = callbackAddr.call{value: 0}(
            abi.encodeWithSelector(callbackFunctionId, requestId, data)
        );

        require(success, "Callback failed");

        emit OracleResponse(requestId);
        return true;
    }
}
