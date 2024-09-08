import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NoData from './no-data.png';
import { ChakraProvider, Container, Heading, FormControl, FormLabel, Input, Select, Box, Button, Badge, Text, Icon, Flex, Image, SimpleGrid, useToast, Divider, Card, CardBody, Spinner } from "@chakra-ui/react";
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { FaHome, FaBed, FaBath } from 'react-icons/fa';
import 'react-tabs/style/react-tabs.css';
import './App.css';

const cityMap = {
  "HCM_T5": "Thành phố HCM",
  "HaNoi_T5": "Hà Nội"
};

const districtMap = {
  "quan-1": "Quận 1",
  "quan-2": "Quận 2",
  "quan-3": "Quận 3",
  "quan-4": "Quận 4",
  "quan-5": "Quận 5",
  "quan-6": "Quận 6",
  "quan-7": "Quận 7",
  "quan-8": "Quận 8",
  "quan-9": "Quận 9",
  "quan-10": "Quận 10",
  "quan-11": "Quận 11",
  "quan-12": "Quận 12",
  "binh-tan": "Quận Bình Tân",
  "binh-thanh": "Quận Bình Thạnh",
  "go-vap": "Quận Gò Vấp",
  "phu-nhuan": "Quận Phú Nhuận",
  "tan-binh": "Quận Tân Bình",
  "tan-phu": "Quận Tân Phú",
  "thu-duc": "Quận Thủ Đức",
  "binh-chanh": "Huyện Bình Chánh",
  "can-gio": "Huyện Cần Giờ",
  "cu-chi": "Huyện Củ Chi",
  "hoc-mon": "Huyện Hóc Môn",
  "nha-be": "Huyện Nhà Bè",
  "ba-dinh": "Quận Ba Đình",
  "bac-tu-liem": "Quận Bắc Từ Liêm",
  "cau-giay": "Quận Cầu Giấy",
  "dong-da": "Quận Đống Đa",
  "ha-dong": "Quận Hà Đông",
  "hai-ba-trung": "Quận Hai Bà Trưng",
  "hoan-kiem": "Quận Hoàn Kiếm",
  "hoang-mai": "Quận Hoàng Mai",
  "long-bien": "Quận Long Biên",
  "nam-tu-liem": "Quận Nam Từ Liêm",
  "tay-ho": "Quận Tây Hồ",
  "thanh-xuan": "Quận Thanh Xuân",
  "ba-vi": "Huyện Ba Vì",
  "chuong-my": "Huyện Chương Mỹ",
  "dan-phuong": "Huyện Đan Phượng",
  "dong-anh": "Huyện Đông Anh",
  "gia-lam": "Huyện Gia Lâm",
  "hoai-duc": "Huyện Hoài Đức",
  "me-linh": "Huyện Mê Linh",
  "my-duc": "Huyện Mỹ Đức",
  "phu-xuyen": "Huyện Phú Xuyên",
  "phuc-tho": "Huyện Phúc Thọ",
  "quoc-oai": "Huyện Quốc Oai",
  "soc-son": "Huyện Sóc Sơn",
  "thach-that": "Huyện Thạch Thất",
  "thanh-oai": "Huyện Thanh Oai",
  "thanh-tri": "Huyện Thanh Trì",
  "thuong-tin": "Huyện Thường Tín",
  "ung-hoa": "Huyện Ứng Hòa",
  "son-tay": "Thị xã Sơn Tây"
  // Add all other districts here
};

const propertyTypeMap = {
  'nha-rieng': 'Nhà riêng',
  'dat-dat-nen': 'Đất đai'
};

const booleanMap = {
  1: 'Có',
  0: 'Không'
};

const PropertyCard = ({ location, price, area, image, bedroom, toilet, pricePerM2, published, url }) => (
  <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="5" background="#fff">
    <Box width="100%" height="200px" overflow="hidden">
      <Image src={image} width="100%" height="100%" objectFit="cover" />
    </Box>

    <Box p="6">
      <Box d="flex" alignItems="baseline">
        <Badge borderRadius="full" px="2" colorScheme="teal">
          {location}
        </Badge>
      </Box>

      <Box color="#333">
        Giá: {price} VNĐ
      </Box>

      <Flex color="#333" mt="2" alignItems="center">
        <Icon as={FaHome} />
        <Text ml="2" fontSize="sm">
          {area}
        </Text>
      </Flex>

      <Flex color="#333" mt="2" alignItems="center">
        <Icon as={FaBed} />
        <Text ml="2" fontSize="sm">
          Phòng ngủ: {bedroom}
        </Text>
      </Flex>

      <Flex color="#333" mt="2" alignItems="center">
        <Icon as={FaBath} />
        <Text ml="2" fontSize="sm">
          Toilet: {toilet}
        </Text>
      </Flex>

      <Box color="#333" mt="2">
        Giá/m²: {pricePerM2}
      </Box>

      <Box display='flex' color="#333" mt="2">
        Ngày đăng tin: {published}
      </Box>

      <Box display='flex' justifyContent='center'>
        <Button as="a" href={url} mt="4" colorScheme="teal" target="_blank">
          Xem chi tiết
        </Button>
      </Box>
    </Box>
  </Box>
);

const App = () => {
  const [selectedCity, setSelectedCity] = useState("");
  const [Type, setType] = useState("");
  const [statePrice, setStatePrice] = useState("");
  const [properties, setProperties] = useState({});
  const [arrayData, setArrayData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tabIndex, setTabIndex] = useState(0);
  const [sortValue, setSortValue] = useState(1);

  const toast = useToast();

  const [formData, setFormData] = useState({
    model: '',
    district_name: '',
    type: '',
    area: '',
    floors: '',
    bedroom: '',
    toilet: '',
    facade: '',
    furniture: '',
    status_doc: '',
    market: '',
    hospital: ''
  });

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get('http://127.0.0.1:5000/recommend_listings', {
          params: {
            district_name: arrayData.district_name,
            type: arrayData.type_name,
            area: arrayData.area,
            bedroom: arrayData.bedroom,
            toilet: arrayData.toilet,
            sort_value: sortValue
          },
        });
        setProperties(response.data);
      } catch (error) {
        console.error('Error fetching data', error);
      }
      setLoading(false);
    };

    if (arrayData.district_name) {
      fetchData();
    }
  }, [arrayData, sortValue]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'model') {
      setSelectedCity(value);
    }
    if (name === 'type') {
      setType(value);
    }
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSubmit = {
      ...formData,
      area: parseInt(formData.area, 10),
      floors: parseInt(formData.floors, 10),
      bedroom: parseInt(formData.bedroom, 10),
      toilet: parseInt(formData.toilet, 10),
      facade: parseInt(formData.facade, 10),
      furniture: parseInt(formData.furniture, 10),
      status_doc: parseInt(formData.status_doc, 10),
      market: parseInt(formData.market, 10),
      hospital: parseInt(formData.hospital, 10),
    };
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict_price', dataToSubmit);
      toast({
        title: 'Gửi dữ liệu thành công.',
        description: 'Dữ liệu của bạn đã được gửi thành công.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      setArrayData(response.data);
      setStatePrice(response.data.price);
      setTabIndex(1);  // Switch to the "KẾT QUẢ DỰ ĐOÁN" tab
    } catch (error) {
      toast({
        title: 'Lỗi gửi dữ liệu.',
        description: 'Đã xảy ra lỗi khi gửi dữ liệu. Vui lòng thử lại.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <ChakraProvider>
      <div className="background-container"></div>
      <div className="background-overlay"></div>
      <Box className="content">
        <Tabs selectedIndex={tabIndex} onSelect={index => setTabIndex(index)}>
          <TabList style={{ textAlign: 'center', border: 'none'}}>
            <Tab style={{ background: 'none', fontWeight: 'bold', border: 'none', color: 'white'}}>DỰ ĐOÁN GIÁ NHÀ</Tab>
            <Tab style={{ background: 'none', fontWeight: 'bold', border: 'none', color: 'white' }}>KẾT QUẢ DỰ ĐOÁN</Tab>
          </TabList>
          <TabPanel>
            <Container maxW="4xl" py={10}>
              <Heading textAlign="center" mb={10} color={'white'}>Dự đoán giá nhà</Heading>
              <Card>
                <CardBody>
                  <form onSubmit={handleSubmit}>
                    <Box mb={4}>
                      <FormControl>
                        <FormLabel>Tỉnh thành</FormLabel>
                        <Select
                          borderRadius='18px'
                          name='model'
                          placeholder="--Chọn--"
                          onChange={handleChange}
                        >
                          <option value="HCM_T5">Thành phố HCM</option>
                          <option value="HaNoi_T5">Hà Nội</option>
                        </Select>
                      </FormControl>
                    </Box>

                    {selectedCity === "HCM_T5" && (
                      <Box mb={4}>
                        <FormControl>
                          <FormLabel>Quận huyện (HCM)</FormLabel>
                          <Select borderRadius='18px' onChange={handleChange} name="district_name" placeholder="--Chọn--">
                            <option value="quan-1">Quận 1</option>
                            <option value="quan-2">Quận 2</option>
                            <option value="quan-3">Quận 3</option>
                            <option value="quan-4">Quận 4</option>
                            <option value="quan-5">Quận 5</option>
                            <option value="quan-6">Quận 6</option>
                            <option value="quan-7">Quận 7</option>
                            <option value="quan-8">Quận 8</option>
                            <option value="quan-9">Quận 9</option>
                            <option value="quan-10">Quận 10</option>
                            <option value="quan-11">Quận 11</option>
                            <option value="quan-12">Quận 12</option>
                            <option value="binh-tan">Quận Bình Tân</option>
                            <option value="binh-thanh">Quận Bình Thạnh</option>
                            <option value="go-vap">Quận Gò Vấp</option>
                            <option value="phu-nhuan">Quận Phú Nhuận</option>
                            <option value="tan-binh">Quận Tân Bình</option>
                            <option value="tan-phu">Quận Tân Phú</option>
                            <option value="thu-duc">Quận Thủ Đức</option>
                            <option value="binh-chanh">Huyện Bình Chánh</option>
                            <option value="can-gio">Huyện Cần Giờ</option>
                            <option value="cu-chi">Huyện Củ Chi</option>
                            <option value="hoc-mon">Huyện Hóc Môn</option>
                            <option value="nha-be">Huyện Nhà Bè</option>
                          </Select>
                        </FormControl>
                      </Box>
                    )}

                    {selectedCity === "HaNoi_T5" && (
                      <Box mb={4}>
                        <FormControl>
                          <FormLabel>Quận huyện (Hà Nội)</FormLabel>
                          <Select borderRadius='18px' onChange={handleChange} name="district_name" placeholder="--Chọn--">
                            <option value="ba-dinh">Quận Ba Đình</option>
                            <option value="bac-tu-liem">Quận Bắc Từ Liêm</option>
                            <option value="cau-giay">Quận Cầu Giấy</option>
                            <option value="dong-da">Quận Đống Đa</option>
                            <option value="ha-dong">Quận Hà Đông</option>
                            <option value="hai-ba-trung">Quận Hai Bà Trưng</option>
                            <option value="hoan-kiem">Quận Hoàn Kiếm</option>
                            <option value="hoang-mai">Quận Hoàng Mai</option>
                            <option value="long-bien">Quận Long Biên</option>
                            <option value="nam-tu-liem">Quận Nam Từ Liêm</option>
                            <option value="tay-ho">Quận Tây Hồ</option>
                            <option value="thanh-xuan">Quận Thanh Xuân</option>
                            <option value="ba-vi">Huyện Ba Vì</option>
                            <option value="chuong-my">Huyện Chương Mỹ</option>
                            <option value="dan-phuong">Huyện Đan Phượng</option>
                            <option value="dong-anh">Huyện Đông Anh</option>
                            <option value="gia-lam">Huyện Gia Lâm</option>
                            <option value="hoai-duc">Huyện Hoài Đức</option>
                            <option value="me-linh">Huyện Mê Linh</option>
                            <option value="my-duc">Huyện Mỹ Đức</option>
                            <option value="phu-xuyen">Huyện Phú Xuyên</option>
                            <option value="phuc-tho">Huyện Phúc Thọ</option>
                            <option value="quoc-oai">Huyện Quốc Oai</option>
                            <option value="soc-son">Huyện Sóc Sơn</option>
                            <option value="thach-that">Huyện Thạch Thất</option>
                            <option value="thanh-oai">Huyện Thanh Oai</option>
                            <option value="thanh-tri">Huyện Thanh Trì</option>
                            <option value="thuong-tin">Huyện Thường Tín</option>
                            <option value="ung-hoa">Huyện Ứng Hòa</option>
                            <option value="son-tay">Thị xã Sơn Tây</option>
                          </Select>
                        </FormControl>
                      </Box>
                    )}

                    <Flex>
                      <Box w={'50%'} mb={4} mr={2}>
                        <FormControl>
                          <FormLabel>Loại nhà</FormLabel>
                          <Select borderRadius='18px' onChange={handleChange} name="type" placeholder="--Chọn--">
                            <option value="nha-rieng">Nhà riêng</option>
                            <option value="dat-dat-nen">Đất đai</option>
                          </Select>
                        </FormControl>
                      </Box>

                      <Box w={'50%'} mb={4}>
                        <FormControl>
                          <FormLabel>Diện tích (m²)</FormLabel>
                          <Input borderRadius='18px' name='area' type='number' placeholder='Nhập diện tích' onChange={handleChange} />
                        </FormControl>
                      </Box>
                    </Flex>

                    {Type === "nha-rieng" && (
                      <>
                        <Flex>
                          <Box w={'50%'} mb={4} mr={2}>
                            <FormControl>
                              <FormLabel>Số tầng</FormLabel>
                              <Input borderRadius='18px' name='floors' type='number' placeholder='Nhập số tầng' onChange={handleChange} />
                            </FormControl>
                          </Box>

                          <Box w={'50%'} mb={4}>
                            <FormControl>
                              <FormLabel>Độ rộng mặt tiền (m)</FormLabel>
                              <Input borderRadius='18px' name='facade' type='number' placeholder='Nhập mặt tiền' onChange={handleChange} />
                            </FormControl>
                          </Box>
                        </Flex>

                        <Flex>
                          <Box w={'50%'} mb={4} mr={2}>
                            <FormControl>
                              <FormLabel>Số phòng ngủ</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="bedroom" placeholder="--Chọn--" >
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                                <option>5</option>
                                <option>6</option>
                              </Select>
                            </FormControl>
                          </Box>

                          <Box w={'50%'} mb={4}>
                            <FormControl>
                              <FormLabel>Số phòng tắm, phòng vệ sinh</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="toilet" placeholder="--Chọn--" >
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                                <option>5</option>
                                <option>6</option>
                              </Select>
                            </FormControl>
                          </Box>
                        </Flex>

                        <Flex>
                          <Box w={'50%'} mb={4} mr={2}>
                            <FormControl>
                              <FormLabel>Nội thất</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="furniture" placeholder="--Chọn--">
                                <option value="1">Có</option>
                                <option value="0">Không</option>
                              </Select>
                            </FormControl>
                          </Box>

                          <Box w={'50%'} mb={4}>
                            <FormControl>
                              <FormLabel>Tình trạng pháp lý</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="status_doc" placeholder="--Chọn--">
                                <option value="1">Có</option>
                                <option value="0">Không</option>
                              </Select>
                            </FormControl>
                          </Box>
                        </Flex>

                        <Flex>
                          <Box w={'50%'} mb={4} mr={2}>
                            <FormControl>
                              <FormLabel> Gần chợ</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="market" placeholder="--Chọn--">
                                <option value="1">Có</option>
                                <option value="0">Không</option>
                              </Select>
                            </FormControl>
                          </Box>

                          <Box w={'50%'} mb={4}>
                            <FormControl>
                              <FormLabel>Gần bệnh viện</FormLabel>
                              <Select borderRadius='18px' onChange={handleChange} name="hospital" placeholder="--Chọn--">
                                <option value="1">Có</option>
                                <option value="0">Không</option>
                              </Select>
                            </FormControl>
                          </Box>
                        </Flex>

                      </>
                    )}

                    <Button type="submit" colorScheme="blue" borderRadius='18px' width='100%' mt={4}>
                      Dự đoán giá
                    </Button>
                  </form>
                </CardBody>
              </Card>
            </Container>
          </TabPanel>
          <TabPanel>
            <Container maxW="4xl" py={10}>
              <Heading textAlign="center" mb={10} color={'white'}>Kết quả dự đoán</Heading>
              {properties?.recommendations?.length > 0 && (
                <Box
                  maxW="600px"
                  mx="auto"
                  p={4}
                  border="1px"
                  borderColor="gray.200"
                  borderRadius="md"
                  boxShadow="md"
                  bg="white"
                >
                  <Text textAlign="center" fontSize="1xl" mb={4}>
                    Lưu ý: Đây chỉ là mức giá tham khảo!
                  </Text>
                  <Text textAlign="center" fontSize="3xl" fontWeight="bold" mb={4}>
                    {statePrice} triệu VNĐ
                  </Text>
                  <SimpleGrid columns={2} spacing={4}>
                    <Flex alignItems="center">
                      <Text fontWeight="bold">Tỉnh thành phố:</Text>
                      <Text ml={2}>{cityMap[formData.model]}</Text>
                    </Flex>
                    <Flex alignItems="center">
                      <Text fontWeight="bold">Quận huyện:</Text>
                      <Text ml={2}>{districtMap[formData.district_name]}</Text>
                    </Flex>
                    <Flex alignItems="center">
                      <Text fontWeight="bold">Loại bất động sản:</Text>
                      <Text ml={2}>{propertyTypeMap[formData.type]}</Text>
                    </Flex>
                    <Flex alignItems="center">
                      <Text fontWeight="bold">Diện tích:</Text>
                      <Text ml={2}>{formData.area} m²</Text>
                    </Flex>
                    {arrayData.type_name === "nha-rieng" && (
                      <>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Số tầng:</Text>
                          <Text ml={2}>{formData.floors}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Mặt tiền:</Text>
                          <Text ml={2}>{formData.facade} m</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Số phòng ngủ:</Text>
                          <Text ml={2}>{formData.bedroom}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Số phòng tắm:</Text>
                          <Text ml={2}>{formData.toilet}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Nội thất:</Text>
                          <Text ml={2}>{booleanMap[formData.furniture]}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Tình trạng pháp lý:</Text>
                          <Text ml={2}>{booleanMap[formData.status_doc]}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Gần chợ:</Text>
                          <Text ml={2}>{booleanMap[formData.market]}</Text>
                        </Flex>
                        <Flex alignItems="center">
                          <Text fontWeight="bold">Gần bệnh viện:</Text>
                          <Text ml={2}>{booleanMap[formData.hospital]}</Text>
                        </Flex>
                      </>
                    )}
                  </SimpleGrid>
                  <Divider my={4} />
                </Box>
              )}
            </Container>

            <Box display="flex" justifyContent="center" alignItems="center" mb={4}>
              <Heading size="lg" color={'white'}>Danh sách gợi ý:</Heading>
              <Box ml={4}>
                <select value={sortValue} onChange={(e) => setSortValue(e.target.value)}>
                  <option value="1">Tin mới nhất</option>
                  <option value="2">Giá tăng dần</option>
                  <option value="3">Giá giảm dần</option>
                  <option value="4">Diện tích tăng dần</option>
                  <option value="5">Diện tích giảm dần</option>
                </select>
              </Box>
            </Box>

            {loading ? (
              <Box display='flex' justifyContent='center' alignItems='center' height='100vh'>
                <Spinner size= 'xl' color='white'/>
              </Box>
            ) : (
              <>
                {properties?.recommendations?.length > 0 ? (
                  <Flex direction="row" wrap="wrap" justify="center" gap="6">
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6} p={6}>
                      {properties?.recommendations?.map((item, index) => (
                        <PropertyCard
                          key={index}
                          location={item?.location}
                          price={item?.price}
                          area={item?.area}
                          image={item?.image_url}
                          bedroom={item?.bedroom}
                          toilet={item?.toilet}
                          pricePerM2={item?.pricePerM2}
                          published={item?.published}
                          url={item?.url}
                        />
                      ))}
                    </SimpleGrid>
                  </Flex>
                ) : (
                  <Box textAlign="center">
                    <Image
                      src={NoData}
                      alt="No Data"
                      maxWidth="300px"
                      height="auto"
                      margin="0 auto"
                      objectFit="contain"
                      borderRadius="md"
                    />
                    <Text color={'white'}>Không có dữ liệu hiển thị</Text>
                  </Box>
                )}
              </>
            )}
          </TabPanel>
        </Tabs>
      </Box>
    </ChakraProvider >
  );
};

export default App;
