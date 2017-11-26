#ifndef _THREAD_POOL_H_
#define _THREAD_POOL_H_
#include <pthread.h>
#include <queue>

struct Task {
	void (*foo)(void*);
	void* arg;
};

class ThreadPool {
  private:
	std::queue<Task*> *tasks;
	pthread_t *workers;

	pthread_mutex_t *m1;
	pthread_mutex_t *m2;
	pthread_mutex_t *m3;

	size_t num_of_wrks;
	size_t num_of_fwrks;
	volatile size_t num_of_ewrks;

	bool is_going_end;
  private:
	struct Outfit {
		ThreadPool *pool;
		pthread_mutex_t *m1;
		pthread_mutex_t *m2;
		pthread_mutex_t *m3;
	};
  private:
	Outfit *outfit;
  private:
	static void *work(void *arg);
	
	static void empty(void *arg);
  public:
	ThreadPool(size_t threads_nm);

	~ThreadPool();

	void submit (Task *t);

	void finit();
  private:
	Task* get_task();

	bool is_end();
	void check_in_queue();
	void release_worker();
};

#endif
