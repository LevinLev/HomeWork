#include "thread_pool.h"
#include <iostream>

void inc(void *arg) {
	Data1 *data = (Data1*) arg;
	for (int i = data->L; i < data->R; i++)
		data->array[i]++;
}

int main() {
	ThreadPool pool(2);
	pool.finit();

	ThreadPool pool1(4);

	Task task[4];
	Data1 data[4];
	int array[12] = {0};
	for (int i = 0 ; i < 4; i++) {
		data[i].array = array;
		data[i].L = i * 3;
		data[i].R = i * 3 + 3;
		task[i].foo = inc;
		task[i].arg = &data[i];
		task[i].is_done = false;
		pool1.submit(task + i);
	}
	pool1.finit();

	for (int i = 0 ; i < 12; i++)
		std::cout << array[i] << " ";
	std::cout << std::endl;

	return 0;
}
