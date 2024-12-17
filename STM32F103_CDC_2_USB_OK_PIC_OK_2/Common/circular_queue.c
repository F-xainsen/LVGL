#include "circular_queue.h"

/**
 * @brief 初始化环形队列    
 * \param queue  队列结构体变量指针
 * \param buffer 队列缓存区地址
 * \param buffer_size   队列最大大小
 */
void queue_init(QueueType_t *queue, uint8_t *buffer, uint32_t buffer_size)
{
    queue->head = 0;
    queue->tail = 0;
    queue->size = buffer_size;
    queue->buffer = buffer;
}
/**
 * @brief 数据入队（向队列尾部插入数据）
 * 
 * \param queue 队列结构体变量指针
 * \param dat  一个字节数据
 * \return QueueStatus_t  入队结果 QUEUE_OK 成功
 */
QueueStatus_t queue_push(QueueType_t *queue, uint8_t dat)
{
    // 计算下一个元素的索引
    uint32_t next_index = (queue->tail + 1)  % queue->size;
    // 队列满(保留一个空位)
    if (next_index == queue->head) {
        return QUEUE_FULL;
    } 
    // 写入数据
    queue->buffer[queue->tail] = dat;
    // 更新队尾指针
    queue->tail = next_index;
    return QUEUE_OK;
}

/**
 * @brief 数据出队（从队首弹出数据）
 * 
 * \param queue 队列结构体变量指针
 * \param pdat  出队数据指针
 * \return QueueStatus_t 
 */
QueueStatus_t queue_pop(QueueType_t *queue, uint8_t *p_dat){
    // 如果head与tail相等，说明队列为空
    if (queue->head == queue->tail) {
        return QUEUE_EMPTY;
    }
    // 取head的数据
    *p_dat = queue->buffer[queue->head];
    // 更新队头指针
    queue->head = (queue->head + 1) % queue->size;
    return QUEUE_OK;
}
/**
 * @brief 获取队列数据个数
 * 
 * \param queue  队列指针
 * \return uint32_t  队列有效数据个数
 */
uint32_t queue_data_count(QueueType_t *queue){
    if (queue->tail >= queue->head){
        // 队尾指针在队头指针后边
        return queue->tail - queue->head;
    }

    // 队尾指针在队头指针前边（转了一圈到了队头指针之前）
    return queue->size + queue->tail - queue->head;
}

/**
 * @brief 压入一组数据
 * 
 * \param queue  队列结构体变量指针
 * \param p_arr  待入队数组指针
 * \param len    待入队数组长度 
 * \return uint32_t 实际写入的数据个数 
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
 * @brief 出队一组数据
 * 
 * \param queue 队列指针
 * \param p_arr 待出队数组指针
 * \param len   待出队数组长度
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
