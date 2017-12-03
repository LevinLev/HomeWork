#ifndef THREAD_POOL_H
#define THREAD_POOL_H
#include <pthread.h>
#include <queue>

class Task {
  private:
	void (*f)(void*);
	void *a;
	
	pthread_mutex_t m;
	pthread_cond_t c;
	
	bool is_done;
  public:
  	Task(void *arg, void (*foo)(void*));
  	~Task();
  	
  	void wait();

  	void *(get_func())(void*);
  	void *get_arg();

  	void set_func(void (*foo)(void*));
  	void set_arg(void *arg);
  	
  	void set_done();
};

void wait(Task *t);

class ThreadPool {
  private:
	std::queue<Task*> *tasks;
	size_t num_of_wrks;
	pthread_t *workers;

	pthread_mutex_t m;

	pthread_cond_t c;
	bool is_queue_empty;
  private:
	static void *work(void *arg);
  public:
	ThreadPool(size_t threads_nm);

	~ThreadPool();

	void submit(Task *t);

	void finit();
  private:
	Task* get_task();
	
	bool is_empty();
	
	pthread_mutex_t *get_mutex();
	pthread_cond_t *get_cond();
};

#endif
