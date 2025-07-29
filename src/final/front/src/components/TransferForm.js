import React, { useState } from 'react';
import {
  Box,
  Input,
  Button,
  useToast,
  Card,
  CardHeader,
  CardBody,
  Text,
  VStack,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import { useWeb3 } from '../context/Web3Context';
import { ethers } from 'ethers';

const TransferForm = () => {
  const { account, provider, error: web3Error } = useWeb3();
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleTransfer = async (e) => {
    e.preventDefault();
    if (!recipient || !amount) {
      toast({
        title: 'Error',
        description: 'Please fill in all fields',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      setLoading(true);
      const signer = provider.getSigner();
      const tx = await signer.sendTransaction({
        to: recipient,
        value: ethers.utils.parseEther(amount),
      });

      toast({
        title: 'Transaction Submitted',
        description: 'Please wait for confirmation...',
        status: 'info',
        duration: 5000,
        isClosable: true,
      });

      await tx.wait();

      toast({
        title: 'Success',
        description: `Successfully transferred ${amount} ETH to ${recipient}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      setRecipient('');
      setAmount('');
    } catch (error) {
      console.error('Transfer error:', error);
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  if (!account) {
    return (
      <Box p={5}>
        <Alert status="info">
          <AlertIcon />
          Please connect your wallet to transfer ETH
        </Alert>
      </Box>
    );
  }

  if (web3Error) {
    return (
      <Box p={5}>
        <Alert status="error">
          <AlertIcon />
          {web3Error}
        </Alert>
      </Box>
    );
  }

  return (
    <Card mb={6}>
      <CardHeader>
        <Text fontSize="xl" color="blue.500">Transfer ETH</Text>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleTransfer}>
          <VStack spacing={4} align="stretch">
            <Box>
              <Text color="gray.600" mb={2}>Recipient Address</Text>
              <Input
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
                placeholder="0x..."
                size="lg"
              />
            </Box>
            <Box>
              <Text color="gray.600" mb={2}>Amount (ETH)</Text>
              <Input
                type="number"
                step="0.000001"
                min="0"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                size="lg"
              />
            </Box>
            <Button
              type="submit"
              colorScheme="blue"
              size="lg"
              width="100%"
              isLoading={loading}
              loadingText="Transferring..."
            >
              TRANSFER
            </Button>
          </VStack>
        </form>
      </CardBody>
    </Card>
  );
};

export default TransferForm; 