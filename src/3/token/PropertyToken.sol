// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract RealEstateNFT is ERC721URIStorage, AccessControl {
    using Counters for Counters.Counter;

    bytes32 public constant REGISTRAR_ROLE = keccak256("REGISTRAR_ROLE");
    bytes32 public constant VERIFIED_BUYER_ROLE = keccak256("VERIFIED_BUYER_ROLE");

    Counters.Counter private _tokenIds;

    struct OwnershipRecord {
        address owner;
        uint256 timestamp;
    }


    mapping(uint256 => string) private _propertyAddresses;


    mapping(uint256 => bool) private _transferApproved;


    mapping(uint256 => OwnershipRecord[]) private _ownershipHistory;

    mapping(address => uint256[]) private _ownedTokens;

    constructor() ERC721("PalaceNFT", "PAlC") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(REGISTRAR_ROLE, msg.sender);
    }


    function mintProperty(
        address to,
        string memory tokenURI,
        string memory addressOfProperty
    ) public onlyRole(REGISTRAR_ROLE) returns (uint256) {
        require(hasRole(VERIFIED_BUYER_ROLE, to), "Recipient is not verified");

        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _mint(to, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        _propertyAddresses[newTokenId] = addressOfProperty;

        _ownershipHistory[newTokenId].push(OwnershipRecord({
            owner: to,
            timestamp: block.timestamp
        }));
        _ownedTokens[to].push(newTokenId);

        return newTokenId;
    }


    function approveTransfer(uint256 tokenId) public onlyRole(REGISTRAR_ROLE) {
        _transferApproved[tokenId] = true;
    }

    function revokeTransfer(uint256 tokenId) public onlyRole(REGISTRAR_ROLE) {
        _transferApproved[tokenId] = false;
    }


    function _removeTokenFromOwner(address from, uint256 tokenId) internal {
        uint256[] storage tokens = _ownedTokens[from];
        for (uint256 i = 0; i < tokens.length; i++) {
            if (tokens[i] == tokenId) {
                tokens[i] = tokens[tokens.length - 1];
                tokens.pop();
                break;
            }
        }
    }


    function transferProperty(address from, address to, uint256 tokenId) public {
        require(msg.sender == ownerOf(tokenId),"Not allowed user");
        require(_transferApproved[tokenId], "Transfer not approved");
        require(hasRole(VERIFIED_BUYER_ROLE, to), "Recipient not verified");

        _transferApproved[tokenId] = false;
        _transfer(from, to, tokenId);

        _ownershipHistory[tokenId].push(OwnershipRecord({
            owner: to,
            timestamp: block.timestamp
        }));
        _removeTokenFromOwner(from, tokenId);
        _ownedTokens[to].push(tokenId);

    }

    function updatePropertyAddress(uint256 tokenId, string memory newAddress)
        public
        onlyRole(REGISTRAR_ROLE)
    {
        _propertyAddresses[tokenId] = newAddress;
    }

    function updateTokenURI(uint256 tokenId, string memory newURI)
        public
        onlyRole(REGISTRAR_ROLE)
    {
        _setTokenURI(tokenId, newURI);
    }


    function getOwnershipHistory(uint256 tokenId)
        public
        view
        returns (OwnershipRecord[] memory)
    {
        return _ownershipHistory[tokenId];
    }


    function getPropertyAddress(uint256 tokenId)
        public
        view
        returns (string memory)
    {
        return _propertyAddresses[tokenId];
    }


    function isTransferApproved(uint256 tokenId)
        public
        view
        returns (bool)
    {
        return _transferApproved[tokenId];
    }
    
    function tokensOfOwner(address owner) public view returns (uint256[] memory) {
        return _ownedTokens[owner];
    }


    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

}
