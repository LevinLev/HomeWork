#include "thread_pool.h"
#include <iostream>

Task::Task() {
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

void Task::set_done() {
	pthread_mutex_lock(&m);
	is_done = true;
	pthread_cond_broadcast(&c);
	pthread_mutex_unlock(&m);
}

void* ThreadPool::work(void *arg) {
	ThreadPool *pool = (ThreadPool*) arg;
	Task *task;

	while (true) {
		task = pool->get_task();
		if (task == NULL)
			break;
		task->func(task->arg);
		pool->set_done(task);
	}

	return NULL;
}

ThreadPool::ThreadPool(size_t threads_nm) {
	tasks = new std::queue<Task*>;
	num_of_wrks = threads_nm;
	workers = new pthread_t[num_of_wrks];
	
	pthread_mutex_init(&m, NULL);
	pthread_cond_init(&c, NULL);
	pthread_cond_init(&c_done, NULL);
	tasks_in_work = 0;
	is_end = false;

	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_create(workers + i, NULL, work, this);
}

ThreadPool::~ThreadPool() {
	delete[] workers;
	delete tasks;

	pthread_mutex_destroy(&m);
	pthread_cond_destroy(&c);
	pthread_cond_destroy(&c_done);
}

void ThreadPool::submit(Task *t) {
	pthread_mutex_lock(&m);
	tasks->push(t);
	pthread_cond_broadcast(&c);
	pthread_mutex_unlock(&m);
}

void ThreadPool::finit() {
	pthread_mutex_lock(&m);
	while (tasks_in_work != 0 || tasks->size() != 0)
		pthread_cond_wait(&c_done, &m);
	is_end = true;
	pthread_cond_broadcast(&c);
	pthread_mutex_unlock(&m);

	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_join(workers[i], NULL);
}

Task* ThreadPool::get_task() {
	pthread_mutex_lock(&m);
	Task *task;

	while (tasks->size() == 0 && !is_end)
		pthread_cond_wait(&c, &m);

	if (is_end == true) {
		pthread_mutex_unlock(&m);
		return NULL;
	}

	task = tasks->front();
	tasks->pop();
	tasks_in_work++;

	pthread_mutex_unlock(&m);

	return task;
}

void ThreadPool::set_done(Task *t) {
	pthread_mutex_lock(&m);
	tasks_in_work--;
	pthread_cond_broadcast(&c_done);
	pthread_mutex_unlock(&m);

	t->set_done();
}
