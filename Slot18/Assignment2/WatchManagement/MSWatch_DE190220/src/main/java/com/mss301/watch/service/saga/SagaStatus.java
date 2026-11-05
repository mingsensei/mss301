package com.mss301.watch.service.saga;

/**
 * 6 trạng thái của Saga Orchestrator (Chapter 06 - Slide 27):
 * <ul>
 *   <li>PENDING      : vừa khởi tạo bản ghi SagaStates, chuẩn bị chạy bước 1</li>
 *   <li>EXECUTING    : đang chạy các bước tiến (forward steps)</li>
 *   <li>COMPLETED    : tất cả các bước đã commit thành công</li>
 *   <li>FAILED       : một bước bị lỗi, chuẩn bị chạy bù trừ</li>
 *   <li>COMPENSATING : đang chạy các bước bù trừ (compensating steps)</li>
 *   <li>COMPENSATED  : toàn bộ các bước đã commit được hoàn tác thành công</li>
 * </ul>
 */
// [TODO-6.3: 6 trạng thái Saga (Slide 27)]
public enum SagaStatus {
    PENDING,
    EXECUTING,
    COMPLETED,
    FAILED,
    COMPENSATING,
    COMPENSATED
}
