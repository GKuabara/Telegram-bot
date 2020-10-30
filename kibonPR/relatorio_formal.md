<center>
	<h3>
		Universidade de São Paulo (USP)<br>
		Instituto de Ciências Matemáticas e de Computação (ICMC)<br>        
	</h3>
	<h3>
		Bacharelado de Ciências de Computação<br>
		Disciplina: Laboratório de Introdução à Ciência da Computação II<br>
		Professor: Leonardo Pereira<br><br>
		Aluno: Guilherme Machado Rios (11222839)
	</h3>
	<h1>
		Contagem de operações e tempo de execução
	</h1>
</center>

Sendo


```c
int recursive_bin_search(int *vector, int key, int low, int high) {
	if (low > high) return NOT_FOUND; //

	int mid = (low + high) / 2;

	if (vector[mid] < key) {
		return recursive_bin_search(vector, key, mid + 1, high);
	}
	else if (vector[mid] > key) {
		return recursive_bin_search(vector, key, low, mid - 1);
	}

	return mid + 1;
}
```

```c
int iterative_bin_search(int *vector, int key, int low, int high) {
	int mid;
	while (low <= high) { 
		mid = (low + high) / 2;

		if (vector[mid] < key) low = mid + 1;
		else if (vector[mid] > key) high = mid - 1;
		else return mid + 1;
	}

	return NOT_FOUND;
}
```
```c
int sequential_search(int *vector, int key, int vector_len) {
	for (int i = 0; i < vector_len; i++) {
		if (vector[i] == key) return i + 1;
	}

	return NOT_FOUND;
}
```