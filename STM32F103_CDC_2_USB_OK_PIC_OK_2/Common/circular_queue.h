#ifndef __CIRCULAR_QUEUE_H__
#define __CIRCULAR_QUEUE_H__

#include <stdint.h>

typedef struct {
    uint32_t head;      // 队头指针
    uint32_t tail;      // 队尾指针
    uint32_t size;      // 队列大小
    uint8_t *buffer;    // 队列缓冲区
} QueueType_t;

typedef enum {

    QUEUE_OK = 0,  // 成功
    QUEUE_FULL,   // 队列满
    QUEUE_EMPTY,  // 队列空
    QUEUE_ERROR   // 错误

} QueueStatus_t;

// 初始化
void queue_init(QueueType_t *queue, uint8_t *buffer, uint32_t buffer_size);

// 入队
QueueStatus_t queue_push(QueueType_t *queue, uint8_t dat);

// 出队
QueueStatus_t queue_pop(QueueType_t *queue, uint8_t *p_dat);

// 压入一组数据
uint32_t queue_push_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len);

// 出队一组数据
uint32_t queue_pop_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len);

// 获取队列数据个数
uint32_t queue_data_count(QueueType_t *queue);

#endif