#include <Python.h>

static PyObject* spam_plus(PyObject* self, PyObject* args) {
    PyObject* counts;

    // ���ڷ� ���޵� ����Ʈ ��������
    if (!PyArg_ParseTuple(args, "O", &counts)) {
        return NULL;
    }

    // ����Ʈ�� ���� Ȯ��
    Py_ssize_t len = PyList_Size(counts);

    int sum = 0;

    // ����Ʈ�� �� ��Ҹ� ��ȸ�ϸ� ���� ����
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

    // ��� ��ȯ
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
