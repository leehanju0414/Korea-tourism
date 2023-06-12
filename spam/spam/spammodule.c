#include <Python.h>

static PyObject* spam_plus(PyObject* self, PyObject* args) {
    PyObject* counts;

    // 인자로 전달된 리스트 가져오기
    if (!PyArg_ParseTuple(args, "O", &counts)) {
        return NULL;
    }

    // 리스트의 길이 확인
    Py_ssize_t len = PyList_Size(counts);

    int sum = 0;

    // 리스트의 각 요소를 순회하며 덧셈 수행
    for (Py_ssize_t i = 0; i < len; ++i) {
        PyObject* item = PyList_GetItem(counts, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "List must contain integers only");
            return NULL;
        }
        long value = PyLong_AsLong(item);
        if (value == -1 && PyErr_Occurred()) {
            return NULL;
        }
        sum += value;
    }

    // 결과 반환
    return PyLong_FromLong(sum);
}

static PyMethodDef SpamMethods[] = {
    {"spam_plus", spam_plus, METH_VARARGS, "Sum the elements in a list."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "Test module",
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_spam(void) {
    return PyModule_Create(&spammodule);
}
