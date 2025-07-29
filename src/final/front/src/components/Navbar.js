import React from 'react';
import {
  Box,
  Flex,
  Button,
  Heading,
  Spacer,
  useColorModeValue,
  Spinner,
  Text,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import { useWeb3 } from '../context/Web3Context';

const Navbar = () => {
  const { account, connectWallet, disconnectWallet, loading, error, isConnected } = useWeb3();
  const bg = useColorModeValue('white', 'gray.800');

  return (
    <Box w="100%" px={4} bg={bg} boxShadow="sm">
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <Heading size="md">Tosh Market</Heading>
        <Spacer />
        
        {error && (
          <Alert status="error" mr={4} maxW="400px">
            <AlertIcon />
            {error}
          </Alert>
        )}

        {isConnected ? (
          <Flex alignItems="center">
            <Text mr={4} fontSize="sm">
              {`${account.slice(0, 6)}...${account.slice(-4)}`}
            </Text>
            <Button
              colorScheme="red"
              variant="outline"
              onClick={disconnectWallet}
              isDisabled={loading}
            >
              Disconnect
            </Button>
          </Flex>
        ) : (
          <Button
            colorScheme="blue"
            onClick={connectWallet}
            isDisabled={loading}
            leftIcon={loading ? <Spinner size="sm" /> : null}
          >
            {loading ? 'Connecting...' : 'Connect Wallet'}
          </Button>
        )}
      </Flex>
    </Box>
  );
};

export default Navbar; 