void handleTickEvent();
uint32_t tickCount;

void Screen1View::handleTickEvent()
{
    Screen1ViewBase::handleTickEvent();
    tickCount ++;
    float rad = (tickCount %360) * 3.14f/180;

    // update and invalidate the clock hand
    txtrHand.updateZAngle(rad);
}

#include <cmsis_os.h>

#include <cmsis_os.h> // Thư viện CMSIS-RTOS
#include <cmath>      // Thư viện toán học cho các phép toán lượng giác (nếu cần)

// Hằng số
constexpr float PI = 3.14159265358979f;  // Giá trị chính xác của PI
constexpr uint32_t TICKS_PER_SECOND = 1000;  // Số tick mỗi giây (cấu hình RTOS)
constexpr uint32_t SECONDS_PER_MINUTE = 60; // Số giây trong một phút

void Screen1View::handleTickEvent()
{
    Screen1ViewBase::handleTickEvent(); // Gọi hàm cơ sở để xử lý tick cơ bản

    // Lấy số tick hiện tại từ hệ thống
    uint32_t currentTick = osKernelGetTickCount();

    // Tính số giây đã trôi qua
    uint32_t secondsElapsed = (currentTick / 1000) % 60;

    // Tính góc dịch chuyển của kim (mỗi giây tương ứng với 6 độ: 360 độ / 60 giây)
    float angleDegrees = secondsElapsed * (360.0f / 60);

    // Chuyển đổi góc từ độ sang radian (nếu cần cho đồ họa)
    float angleRadians = angleDegrees * 3.14f / 180.0f;

    // Cập nhật góc của kim đồng hồ
    txtrHand.updateZAngle(angleRadians);

    // Invalidate vùng hiển thị để vẽ lại kim
    txtrHand.invalidate();
}

GPIO_InitStruct.Pin = GPIO_PIN_0;
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
GPIO_InitStruct.Pull == GPIO_NOPULL;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

osMessageQueueId_t Queue1Handle;
const osMessageQueueAttr_t Queue1_Attributes = {
    .name = "Queue1"
}
osStatus_t r_state;

Queue1Handle = osMessageQueueNew(8, sizeof(uint8_t), &Queue1_Attributes);

if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_SET) {
    uint32_t count = osMessageQueueGetCount(Queue1Handle);
    if (count < 2) {
        uint8_t data = 'P';
        osMessageQueuePut(Queue1Handle, &data, 0 , 10);
    }
}


Unicode::snprintf(scoreTextBuffer, SCORE_TEXT_BUFFER_SIZE, "%d", score); // Chuyển số thành chuỗi
scoreText.setWildcard(scoreTextBuffer);  // Set chuỗi điểm vào TextArea
scoreText.invalidate();  // Làm mới giao diện để hiển thị điểm số mới