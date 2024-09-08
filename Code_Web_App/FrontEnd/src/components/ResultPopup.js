import React from 'react';
import {
    Button,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Text,
} from '@chakra-ui/react';

const ResultPopup = ({ isOpen, onClose }) => {
    //
    return (
        <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader textAlign={'center'}>Kết quả dự đoán</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <Text fontSize={'20px'}>Mức giá: 200.000Đ</Text>
                    <Text fontSize={'20px'}>Số tầng: 2</Text>
                    <Text fontSize={'20px'}>Diện tích: 2</Text>
                    <Text fontSize={'20px'}>Hướng ban công: 2</Text>
                    <Text fontSize={'20px'}>Pháp lý: 2</Text>
                    <Text fontSize={'20px'}>Số phòng ngủ: 2</Text>
                    <Text fontSize={'20px'}>Nội thất: 2</Text>
                    <Text fontSize={'20px'}>Tỉnh thành: 2</Text>
                    <Text fontSize={'20px'}>Quận huyện: 2</Text>
                    <Text fontSize={'20px'}>Phòng tắm: 2</Text>
                </ModalBody>
                <ModalFooter>
                    <Button colorScheme="red" mr={3} onClick={onClose}>
                        Chi tiết kết quả dự đoán
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default ResultPopup;
