#ifndef __CIRCULAR_QUEUE_H__
#define __CIRCULAR_QUEUE_H__

#include <stdint.h>

typedef struct {
    uint32_t head;      // ��ͷָ��
    uint32_t tail;      // ��βָ��
    uint32_t size;      // ���д�С
    uint8_t *buffer;    // ���л�����
} QueueType_t;

typedef enum {

    QUEUE_OK = 0,  // �ɹ�
    QUEUE_FULL,   // ������
    QUEUE_EMPTY,  // ���п�
    QUEUE_ERROR   // ����

} QueueStatus_t;

// ��ʼ��
void queue_init(QueueType_t *queue, uint8_t *buffer, uint32_t buffer_size);

// ���
QueueStatus_t queue_push(QueueType_t *queue, uint8_t dat);

// ����
QueueStatus_t queue_pop(QueueType_t *queue, uint8_t *p_dat);

// ѹ��һ������
uint32_t queue_push_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len);

// ����һ������
uint32_t queue_pop_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len);

// ��ȡ�������ݸ���
uint32_t queue_data_count(QueueType_t *queue);

#endif