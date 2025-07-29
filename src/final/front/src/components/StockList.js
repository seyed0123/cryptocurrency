import React, { useState, useEffect } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Input,
  Select,
  HStack,
  useToast,
  Text,
  Alert,
  AlertIcon,
  Spinner,
  Center,
  Card,
  CardHeader,
  CardBody,
} from '@chakra-ui/react';
import { useWeb3 } from '../context/Web3Context';
import { ethers } from 'ethers';

// Predefined stock symbols to check
const STOCK_SYMBOLS = ['OPEN','INTC','AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX'];

const StockList = () => {
  const { account, stockMarketContract, getTokenContract, error: web3Error } = useWeb3();
  const [stocks, setStocks] = useState([]);
  const [userStocks, setUserStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  const fetchStockData = async (symbol) => {
    try {
      const stockData = await stockMarketContract.stocks(symbol);
      const tokenContract = await getTokenContract(stockData.token);
      const balance = account ? await tokenContract.balanceOf(account) : 0;
      
      return {
        symbol,
        name: stockData.name,
        price: ethers.utils.formatUnits(stockData.lastPrice, 8),
        balance: ethers.utils.formatEther(balance),
        lastUpdated: new Date(stockData.lastUpdated.toNumber() * 1000).toLocaleString(),
      };
    } catch (error) {
      console.error(`Error fetching stock data for ${symbol}:`, error);
      return null;
    }
  };

  const loadStocks = async () => {
    try {
      setError(null);
      setLoading(true);
      
      if (!stockMarketContract) {
        throw new Error("Contract not initialized");
      }

      // Check predefined stock symbols
      const registeredStocks = [];
      for (const symbol of STOCK_SYMBOLS) {
        try {
          const isRegistered = await stockMarketContract.registered(symbol);
          if (isRegistered) {
            registeredStocks.push(symbol);
          }
        } catch (error) {
          console.error(`Error checking registration for ${symbol}:`, error);
        }
      }

      // If no predefined stocks are found, try getting stocks from events
      if (registeredStocks.length === 0) {
        try {
          const filter = stockMarketContract.filters.StockAdded();
          const events = await stockMarketContract.queryFilter(filter);
          for (const event of events) {
            const symbol = event.args.symbol;
            if (!registeredStocks.includes(symbol)) {
              registeredStocks.push(symbol);
            }
          }
        } catch (error) {
          console.error('Error fetching stock events:', error);
        }
      }

      const stockData = await Promise.all(
        registeredStocks.map(symbol => fetchStockData(symbol))
      );
      
      const validStocks = stockData.filter(stock => stock !== null);
      setStocks(validStocks);
      
      // Set user stocks (stocks with non-zero balance)
      setUserStocks(validStocks.filter(stock => parseFloat(stock.balance) > 0));
    } catch (error) {
      console.error('Error loading stocks:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (stockMarketContract && account) {
      loadStocks();
    }
  }, [stockMarketContract, account]);

  const handleBuy = async () => {
    if (!selectedStock || !amount) {
      toast({
        title: 'Error',
        description: 'Please select a stock and enter an amount',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      const stock = stocks.find(s => s.symbol === selectedStock);
      const totalPrice = parseFloat(stock.price) * parseFloat(amount);
      
      const tx = await stockMarketContract.buyStock(
        selectedStock,
        ethers.utils.parseEther(amount.toString()),
        { value: ethers.utils.parseEther(totalPrice.toString()) }
      );
      
      toast({
        title: 'Transaction Submitted',
        description: 'Please wait for confirmation...',
        status: 'info',
        duration: 5000,
        isClosable: true,
      });

      await tx.wait();

      toast({
        title: 'Purchase Successful',
        description: `Successfully bought ${amount} ${selectedStock} shares`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      loadStocks();
      setAmount('');
    } catch (error) {
      console.error('Error buying stock:', error);
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleSell = async () => {
    if (!selectedStock || !amount) {
      toast({
        title: 'Error',
        description: 'Please select a stock and enter an amount',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      const tx = await stockMarketContract.sellStock(
        selectedStock,
        ethers.utils.parseEther(amount.toString())
      );
      
      toast({
        title: 'Transaction Submitted',
        description: 'Please wait for confirmation...',
        status: 'info',
        duration: 5000,
        isClosable: true,
      });

      await tx.wait();

      toast({
        title: 'Sale Successful',
        description: `Successfully sold ${amount} ${selectedStock} shares`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      loadStocks();
      setAmount('');
    } catch (error) {
      console.error('Error selling stock:', error);
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (!account) {
    return (
      <Box p={5}>
        <Alert status="info">
          <AlertIcon />
          Please connect your wallet to view stocks
        </Alert>
      </Box>
    );
  }

  if (loading) {
    return (
      <Center p={5}>
        <Spinner size="xl" />
      </Center>
    );
  }

  if (error || web3Error) {
    return (
      <Box p={5}>
        <Alert status="error">
          <AlertIcon />
          {error || web3Error}
        </Alert>
      </Box>
    );
  }

  return (
    <>
      <Card mb={6}>
        <CardHeader>
          <Text fontSize="xl" color="blue.500">Your Holdings</Text>
        </CardHeader>
        <CardBody>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Symbol</Th>
                <Th>Shares Owned</Th>
                <Th>Current Value (ETH)</Th>
              </Tr>
            </Thead>
            <Tbody>
              {userStocks.map((stock) => (
                <Tr key={stock.symbol}>
                  <Td>{stock.symbol}</Td>
                  <Td>{parseFloat(stock.balance).toFixed(4)}</Td>
                  <Td>{(parseFloat(stock.balance) * parseFloat(stock.price)).toFixed(8)}</Td>
                </Tr>
              ))}
              {userStocks.length === 0 && (
                <Tr>
                  <Td colSpan={3} textAlign="center">No holdings yet</Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </CardBody>
      </Card>

      <Card mb={6}>
        <CardHeader>
          <Text fontSize="xl" color="blue.500">Available Stocks</Text>
        </CardHeader>
        <CardBody>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Symbol</Th>
                <Th>Name</Th>
                <Th>Price (ETH)</Th>
                <Th>Last Updated</Th>
              </Tr>
            </Thead>
            <Tbody>
              {stocks.map((stock) => (
                <Tr key={stock.symbol}>
                  <Td>{stock.symbol}</Td>
                  <Td>{stock.name}</Td>
                  <Td>{parseFloat(stock.price).toFixed(8)}</Td>
                  <Td>{stock.lastUpdated}</Td>
                </Tr>
              ))}
              {stocks.length === 0 && (
                <Tr>
                  <Td colSpan={4} textAlign="center">No stocks available</Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
          <Text fontSize="xl" color="blue.500">Trade Stocks</Text>
        </CardHeader>
        <CardBody>
          <HStack spacing={4} align="flex-end">
            <Box>
              <Text mb={2}>Stock Symbol</Text>
              <Select
                value={selectedStock}
                onChange={(e) => setSelectedStock(e.target.value)}
                placeholder="Select stock"
                w="200px"
              >
                {stocks.map((stock) => (
                  <option key={stock.symbol} value={stock.symbol}>
                    {stock.symbol}
                  </option>
                ))}
              </Select>
            </Box>
            <Box>
              <Text mb={2}>Amount</Text>
              <Input
                type="number"
                min="0"
                step="0.000001"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                w="200px"
              />
            </Box>
            <Button
              colorScheme="green"
              onClick={handleBuy}
              isDisabled={!selectedStock || !amount}
            >
              BUY
            </Button>
            <Button
              colorScheme="red"
              onClick={handleSell}
              isDisabled={!selectedStock || !amount || !userStocks.find(s => s.symbol === selectedStock && parseFloat(s.balance) >= parseFloat(amount))}
            >
              SELL
            </Button>
          </HStack>
        </CardBody>
      </Card>
    </>
  );
};

export default StockList;