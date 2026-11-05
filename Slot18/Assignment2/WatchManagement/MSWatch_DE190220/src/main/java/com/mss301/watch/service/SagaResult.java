package com.mss301.watch.service;

// [TODO-6.14: kết quả bọc sagaId và dữ liệu trả về cho controller]
public record SagaResult<T>(String sagaId, T body) {
}
