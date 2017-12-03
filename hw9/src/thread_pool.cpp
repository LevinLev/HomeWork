#include "thread_pool.h"
#include <iostream>

Task::Task(void *arg, void (*foo)(void*)): 
										   f(foo),
										   a(arg) {
	pthread_mutex_init(&m, NULL);
	pthread_cond_init(&c, NULL);
	is_done = false;
}

Task::~Task() {
	pthread_mutex_destroy(&m);
	pthread_cond_destroy(&c);
}

void Task::wait() {
	pthread_mutex_lock(&m);
	while (is_done == false)
		pthread_cond_wait(&c, &m);	
	pthread_mutex_unlock(&m);
}

void *(Task::get_func())(void*) {
	return f;
}

void *Task::get_arg() {
	return a;
}

void Task::set_func(void (*foo)(void*)) {
	f = foo;
}

void Task::set_arg(void *arg) {
	a = arg;
}

void Task::set_done() {
	pthread_mutex_lock(&m);
	is_done = true;
	pthread_cond_signal(&c);
	pthread_mutex_unlock(&m);
}

void* ThreadPool::work(void *arg) {
	ThreadPool *pool = (ThreadPool*) arg;
	pthread_mutex_t *m = pool->get_mutex();
	pthread_cond_t *c = pool->get_cond();

	Task *task;
	void (*target)(void*);
	void *tool;

	while (true) {
		pthread_mutex_lock(m);
		while (pool->is_empty())
			pthread_cond_wait(c, m);
	
		task = pool->get_task();
		pthread_mutex_unlock(m);

		target = task->get_func();
		tool = task->get_arg();
		target(tool);

		task->set_done();
	}

	return NULL;
}

ThreadPool::ThreadPool(size_t threads_nm) {
	tasks = new std::queue<Task*>;
	num_of_wrks = threads_nm;
	workers = new pthread_t[num_of_wrks];
	
	pthread_mutex_init(&m, NULL);
	pthread_cond_init(&c, NULL);
	is_queue_empty = true;
	pthread_cond_init(&c, NULL);

	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_create(workers + i, NULL, work, this);
}

ThreadPool::~ThreadPool() {
	delete[] workers;
	delete tasks;

	pthread_mutex_destroy(&m);
	pthread_cond_destroy(&c);
}

void ThreadPool::submit(Task *t) {
	pthread_mutex_lock(&m);
	is_queue_empty = false;
	pthread_cond_signal(&c);
	pthread_mutex_unlock(&m);
}

void ThreadPool::finit() {
	pthread_mutex_lock(&m);
	while(!is_queue_empty)
		pthread_cond_wait(&c, &m);
	pthread_mutex_unlock(&m);
	
	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_join(workers[i], NULL);
}

Task* ThreadPool::get_task() {
	Task *task;

	task = tasks->front();
	tasks->pop();

	return task;
}

bool ThreadPool::is_empty() {
	return is_queue_empty;
}

pthread_mutex_t *ThreadPool::get_mutex() {
	return &m;
}

pthread_cond_t *ThreadPool::get_cond() {
	return &c;
}
