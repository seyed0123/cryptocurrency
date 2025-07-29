import React from 'react';
import { ChakraProvider, Box, Container, theme } from '@chakra-ui/react';
import { Web3Provider } from './context/Web3Context';
import Navbar from './components/Navbar';
import WalletInfo from './components/WalletInfo';
import StockList from './components/StockList';
import TransferForm from './components/TransferForm';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Web3Provider>
        <Box minH="100vh" bg="gray.50">
          <Navbar />
          <Container maxW="container.xl" py={8}>
            <Box display={{ base: 'block', md: 'flex' }} gap={8}>
              <Box flex="1" mb={{ base: 8, md: 0 }}>
                <WalletInfo />
                <TransferForm />
              </Box>
              <Box flex="2">
                <StockList />
              </Box>
            </Box>
          </Container>
        </Box>
      </Web3Provider>
    </ChakraProvider>
  );
}

export default App; 