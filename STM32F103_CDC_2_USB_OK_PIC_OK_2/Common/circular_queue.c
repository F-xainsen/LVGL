#include "circular_queue.h"

/**
 * @brief ��ʼ�����ζ���    
 * \param queue  ���нṹ�����ָ��
 * \param buffer ���л�������ַ
 * \param buffer_size   ��������С
 */
void queue_init(QueueType_t *queue, uint8_t *buffer, uint32_t buffer_size)
{
    queue->head = 0;
    queue->tail = 0;
    queue->size = buffer_size;
    queue->buffer = buffer;
}
/**
 * @brief ������ӣ������β���������ݣ�
 * 
 * \param queue ���нṹ�����ָ��
 * \param dat  һ���ֽ�����
 * \return QueueStatus_t  ��ӽ�� QUEUE_OK �ɹ�
 */
QueueStatus_t queue_push(QueueType_t *queue, uint8_t dat)
{
    // ������һ��Ԫ�ص�����
    uint32_t next_index = (queue->tail + 1)  % queue->size;
    // ������(����һ����λ)
    if (next_index == queue->head) {
        return QUEUE_FULL;
    } 
    // д������
    queue->buffer[queue->tail] = dat;
    // ���¶�βָ��
    queue->tail = next_index;
    return QUEUE_OK;
}

/**
 * @brief ���ݳ��ӣ��Ӷ��׵������ݣ�
 * 
 * \param queue ���нṹ�����ָ��
 * \param pdat  ��������ָ��
 * \return QueueStatus_t 
 */
QueueStatus_t queue_pop(QueueType_t *queue, uint8_t *p_dat){
    // ���head��tail��ȣ�˵������Ϊ��
    if (queue->head == queue->tail) {
        return QUEUE_EMPTY;
    }
    // ȡhead������
    *p_dat = queue->buffer[queue->head];
    // ���¶�ͷָ��
    queue->head = (queue->head + 1) % queue->size;
    return QUEUE_OK;
}
/**
 * @brief ��ȡ�������ݸ���
 * 
 * \param queue  ����ָ��
 * \return uint32_t  ������Ч���ݸ���
 */
uint32_t queue_data_count(QueueType_t *queue){
    if (queue->tail >= queue->head){
        // ��βָ���ڶ�ͷָ����
        return queue->tail - queue->head;
    }

    // ��βָ���ڶ�ͷָ��ǰ�ߣ�ת��һȦ���˶�ͷָ��֮ǰ��
    return queue->size + queue->tail - queue->head;
}

/**
 * @brief ѹ��һ������
 * 
 * \param queue  ���нṹ�����ָ��
 * \param p_arr  ���������ָ��
 * \param len    ��������鳤�� 
 * \return uint32_t ʵ��д������ݸ��� 
 */
uint32_t queue_push_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len){
    uint32_t i;
    for(i = 0; i < len; i++){
        if (queue_push(queue, p_arr[i]) == QUEUE_FULL){
            break;
        }
    }
    return i;
}

/**
 * @brief ����һ������
 * 
 * \param queue ����ָ��
 * \param p_arr ����������ָ��
 * \param len   ���������鳤��
 * \return QueueStatus_t 
 */
uint32_t queue_pop_array(QueueType_t *queue, uint8_t *p_arr, uint32_t len){

    uint32_t i;
    for(i = 0; i < len; i++){
        if (queue_pop(queue, &p_arr[i]) == QUEUE_EMPTY){
            break;
        }
    }
    return i;
}
