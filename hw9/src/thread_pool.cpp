#include "thread_pool.h"
#include <iostream>

void wait(Task *t) {
	while (t->is_done == false) {
		//wait
	}
}

void* ThreadPool::work(void *arg) {
	Outfit *outfit = (Outfit*) arg;
	pthread_mutex_t *m1 = outfit->m1;
	pthread_mutex_t *m2 = outfit->m2;
	pthread_mutex_t *m3 = outfit->m3;
	ThreadPool* pool = outfit->pool;

	bool is_worktime = true;
	Task *task;
	void (*target)(void*);
	void *tool;

	while (is_worktime) {
		pthread_mutex_lock(m1);
		task = pool->get_task();
		pthread_mutex_unlock(m1);

		target = *(task->foo);
		tool = task->arg;
		target(tool);
		task->is_done = true;
		if (target == empty)
			delete task;

		pthread_mutex_lock(m2);
		pool->check_in_queue();
		pthread_mutex_unlock(m2);

		pthread_mutex_lock(m3);
		is_worktime = !pool->is_end();
		pthread_mutex_unlock(m3);
	}

	pthread_mutex_lock(m2);
	pool->release_worker();
	pthread_mutex_unlock(m2);

	return NULL;
}	

void ThreadPool::empty(void *arg) {
	//DO NOTHING
}

ThreadPool::ThreadPool(size_t threads_nm) {
	tasks = new std::queue<Task*>;
	num_of_wrks = threads_nm;
	workers = new pthread_t[num_of_wrks];
	
	pthread_mutex_init(&m1, NULL);
	pthread_mutex_init(&m2, NULL);
	pthread_mutex_init(&m3, NULL);

	outfit = new Outfit;
	outfit->pool = this;
	outfit->m1 = &m1;
	outfit->m2 = &m2;
	outfit->m3 = &m3;

	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_create(workers + i, NULL, work, outfit);

	is_going_end = false;
	num_of_fwrks = num_of_wrks;
	num_of_ewrks = 0;
}

ThreadPool::~ThreadPool() {
	delete[] workers;
	delete tasks;

	pthread_mutex_destroy(&m1);
	pthread_mutex_destroy(&m2);
	pthread_mutex_destroy(&m3);

	delete outfit;
}

void ThreadPool::submit(Task *t) {
	if (is_going_end == false)
		tasks->push(t);
}

void ThreadPool::finit() {
	is_going_end = true;

	while (num_of_ewrks < num_of_wrks) {
		//wait
	}

	for (size_t i = 0; i < num_of_wrks; i++)
		pthread_join(workers[i], NULL);
}

Task* ThreadPool::get_task() {
	Task *task;

	if (tasks->size() == 0) {
		task = new Task;
		task->foo = &empty;
		task->arg = NULL;
		task->is_done = false;
	} else {
		task = tasks->front();
		tasks->pop();
	}

	num_of_fwrks--;

	return task;
}

bool ThreadPool::is_end() {
	return is_going_end && num_of_fwrks >= tasks->size();
}

void ThreadPool::check_in_queue() {
	num_of_fwrks++;
}

void ThreadPool::release_worker() {
	num_of_ewrks++;
}
