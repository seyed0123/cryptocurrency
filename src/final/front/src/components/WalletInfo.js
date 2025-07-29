import React, { useState, useEffect } from 'react';
import {
  Box,
  Text,
  Card,
  CardHeader,
  CardBody,
  useColorModeValue,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import { useWeb3 } from '../context/Web3Context';
import { ethers } from 'ethers';

const WalletInfo = () => {
  const { account, provider, error } = useWeb3();
  const [balance, setBalance] = useState('0');
  const [balanceError, setBalanceError] = useState(null);

  useEffect(() => {
    const fetchBalance = async () => {
      if (account && provider) {
        try {
          setBalanceError(null);
          const balance = await provider.getBalance(account);
          setBalance(ethers.utils.formatEther(balance));
        } catch (error) {
          console.error('Error fetching balance:', error);
          setBalanceError('Failed to fetch wallet balance');
          setBalance('0');
        }
      }
    };

    fetchBalance();
    
    // Set up an interval to fetch balance every 30 seconds
    const interval = setInterval(fetchBalance, 30000);
    
    return () => clearInterval(interval);
  }, [account, provider]);

  if (!account) {
    return (
      <Box p={5}>
        <Alert status="info">
          <AlertIcon />
          Please connect your wallet to view your balance
        </Alert>
      </Box>
    );
  }

  if (error || balanceError) {
    return (
      <Box p={5}>
        <Alert status="error">
          <AlertIcon />
          {error || balanceError}
        </Alert>
      </Box>
    );
  }

  return (
    <Card mb={6}>
      <CardHeader>
        <Text fontSize="xl" color="blue.500">Wallet Information</Text>
      </CardHeader>
      <CardBody>
        <Box>
          <Text color="gray.600" mb={2}>Address:</Text>
          <Text>{account}</Text>
        </Box>
        <Box mt={4}>
          <Text color="gray.600" mb={2}>Balance:</Text>
          <Text fontSize="2xl" color="blue.500">{parseFloat(balance).toFixed(4)} ETH</Text>
        </Box>
      </CardBody>
    </Card>
  );
};

export default WalletInfo; 