#ifndef THREAD_POOL_H
#define THREAD_POOL_H
#include <pthread.h>
#include <queue>

class Task {
  public:
	void (*func)(void*);
	void *arg;
  private:	
	pthread_mutex_t m;
	pthread_cond_t c;
	
	bool is_done;
  public:
  	Task();
  	~Task();
  	
  	void wait();
  	
  	void set_done();
};

class ThreadPool {
  private:
	std::queue<Task*> *tasks;
	size_t num_of_wrks;
	pthread_t *workers;

	pthread_mutex_t m;

	pthread_cond_t c;
	bool is_end;

	pthread_cond_t c_done;
	size_t tasks_in_work;
  private:
	static void *work(void *arg);
  public:
	ThreadPool(size_t threads_nm);

	~ThreadPool();

	void submit(Task *t);
	
	void set_done(Task* t);

	void finit();
  private:
	Task* get_task();
};

#endif
