import React, { createContext, useContext, useState, useEffect } from 'react';
import { ethers } from 'ethers';
import StockMarketABI from '../contracts/StockMarket.json';
import StockTokenABI from '../contracts/StockToken.json';

const Web3Context = createContext();

export const useWeb3 = () => {
  const context = useContext(Web3Context);
  if (!context) {
    throw new Error('useWeb3 must be used within a Web3Provider');
  }
  return context;
};

export const Web3Provider = ({ children }) => {
  const [account, setAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [stockMarketContract, setStockMarketContract] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chainId, setChainId] = useState(null);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const SEPOLIA_CHAIN_ID = '0xaa36a7';
  const SEPOLIA_DECIMAL_CHAIN_ID = 11155111;
  const STOCK_MARKET_ADDRESS = '0x2c2dd22be8d0456f3ba7597e7e19293d8e965ffa';

  const resetState = () => {
    setAccount(null);
    setProvider(null);
    setStockMarketContract(null);
    setChainId(null);
    setError(null);
    setIsConnected(false);
    setLoading(false);
  };

  const handleError = (error) => {
    console.error('Error:', error);
    let message = 'An unknown error occurred';
    
    if (error.code === 4001) {
      message = 'User rejected the connection';
    } else if (error.code === -32002) {
      message = 'Please check your wallet - a connection request may be pending';
    } else if (error.message) {
      message = error.message;
    }

    setError(message);
    setLoading(false);
  };

  const getEthereumProvider = () => {
    if (typeof window !== 'undefined' && window.ethereum) {
      // Check if MetaMask is available
      if (window.ethereum.isMetaMask) {
        return window.ethereum;
      }
      // Check if OKX Wallet is available
      if (window.okxwallet) {
        return window.okxwallet;
      }
      // Use any available provider
      return window.ethereum;
    }
    throw new Error('Please install MetaMask or another Web3 wallet');
  };

  const checkAndSwitchNetwork = async (ethereumProvider) => {
    try {
      const provider = new ethers.providers.Web3Provider(ethereumProvider);
      const network = await provider.getNetwork();
      
      if (network.chainId !== SEPOLIA_DECIMAL_CHAIN_ID) {
        try {
          await ethereumProvider.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: SEPOLIA_CHAIN_ID }],
          });
          // Wait a bit for the network switch to complete
          await new Promise(resolve => setTimeout(resolve, 1000));
          return true;
        } catch (switchError) {
          if (switchError.code === 4902) {
            try {
              await ethereumProvider.request({
                method: 'wallet_addEthereumChain',
                params: [{
                  chainId: SEPOLIA_CHAIN_ID,
                  chainName: 'Sepolia Test Network',
                  nativeCurrency: {
                    name: 'Sepolia ETH',
                    symbol: 'ETH',
                    decimals: 18
                  },
                  rpcUrls: ['https://sepolia.infura.io/v3/'],
                  blockExplorerUrls: ['https://sepolia.etherscan.io']
                }]
              });
              // Wait a bit for the network to be added
              await new Promise(resolve => setTimeout(resolve, 1000));
              return true;
            } catch (addError) {
              handleError(new Error('Could not add Sepolia network to wallet'));
              return false;
            }
          }
          handleError(new Error('Could not switch to Sepolia network'));
          return false;
        }
      }
      return true;
    } catch (error) {
      handleError(error);
      return false;
    }
  };

  const setupContractAndListeners = async (ethereumProvider, userAddress) => {
    try {
      const provider = new ethers.providers.Web3Provider(ethereumProvider);
      const signer = provider.getSigner();
      const contract = new ethers.Contract(
        STOCK_MARKET_ADDRESS,
        StockMarketABI.abi,
        signer
      );

      // Test contract connection
      await contract.owner();

      // Set up event listeners
      ethereumProvider.on('accountsChanged', (accounts) => {
        if (accounts.length === 0) {
          resetState();
        } else {
          setAccount(accounts[0]);
        }
      });

      ethereumProvider.on('chainChanged', () => {
        window.location.reload();
      });

      ethereumProvider.on('disconnect', () => {
        resetState();
      });

      setProvider(provider);
      setAccount(userAddress);
      setStockMarketContract(contract);
      setChainId(SEPOLIA_DECIMAL_CHAIN_ID);
      setIsConnected(true);
      setLoading(false);

      return true;
    } catch (error) {
      handleError(error);
      return false;
    }
  };

  const connectWallet = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check if MetaMask is installed
      if (typeof window === 'undefined' || !window.ethereum) {
        throw new Error('Please install MetaMask or another Web3 wallet');
      }

      // Get the appropriate provider
      const ethereumProvider = getEthereumProvider();

      // Request account access
      const accounts = await ethereumProvider.request({ 
        method: 'eth_requestAccounts'
      });
      
      if (!accounts || accounts.length === 0) {
        throw new Error('No accounts found');
      }

      const userAddress = accounts[0];

      // Check and switch network if needed
      const networkOk = await checkAndSwitchNetwork(ethereumProvider);
      if (!networkOk) {
        return;
      }

      // Setup contract and listeners
      await setupContractAndListeners(ethereumProvider, userAddress);

    } catch (error) {
      handleError(error);
      resetState();
    }
  };

  const disconnectWallet = async () => {
    try {
      const ethereumProvider = getEthereumProvider();
      if (ethereumProvider) {
        ethereumProvider.removeAllListeners();
      }
      resetState();
    } catch (error) {
      handleError(error);
    }
  };

  const getTokenContract = async (tokenAddress) => {
    try {
      if (!provider || !isConnected) {
        throw new Error('Wallet not connected');
      }
      const signer = provider.getSigner();
      return new ethers.Contract(tokenAddress, StockTokenABI.abi, signer);
    } catch (error) {
      handleError(error);
      return null;
    }
  };

  useEffect(() => {
    // Auto-connect if wallet is already connected
    if (typeof window !== 'undefined' && window.ethereum && window.ethereum.selectedAddress) {
      connectWallet();
    }

    return () => {
      try {
        const ethereumProvider = getEthereumProvider();
        if (ethereumProvider) {
          ethereumProvider.removeAllListeners();
        }
      } catch (error) {
        console.error('Cleanup error:', error);
      }
    };
  }, []);

  const value = {
    account,
    provider,
    stockMarketContract,
    loading,
    chainId,
    error,
    isConnected,
    connectWallet,
    disconnectWallet,
    getTokenContract
  };

  return (
    <Web3Context.Provider value={value}>
      {children}
    </Web3Context.Provider>
  );
}; 