#include <Python.h>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

static PyObject *ChessError;

static PyObject *
FEN_to_board(PyObject *self, PyObject *args) {
    const char *pos;
    if (!PyArg_ParseTuple(args, "s", &pos)) {
        return NULL;
    }
    
    string position(pos);
    string board_part = position.substr(0, position.find(' '));
    vector<string> rows;
    size_t start = 0;
    size_t end = board_part.find('/');
    
    while (end != string::npos) {
        rows.push_back(board_part.substr(start, end - start));
        start = end + 1;
        end = board_part.find('/', start);
    }
    rows.push_back(board_part.substr(start));

    PyObject *board = PyList_New(rows.size());
    
    for (size_t i = 0; i < rows.size(); ++i) {
        const string &row = rows[i];
        vector<PyObject*> board_row;
        
        for (char c : row) {
            if (isdigit(c)) {
                for (int j = 0; j < c - '0'; ++j) {
                    board_row.push_back(PyUnicode_FromString("0"));
                }
            } else {
                board_row.push_back(PyUnicode_FromStringAndSize(&c, 1));
            }
        }

        PyObject *py_board_row = PyList_New(board_row.size());
        for (size_t j = 0; j < board_row.size(); ++j) {
            PyList_SetItem(py_board_row, j, board_row[j]);
        }
        PyList_SetItem(board, i, py_board_row);
    }

    return board;
}

static PyObject *
board_to_FEN(PyObject *self, PyObject *args) {
    PyObject *board;
    const char *pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    int move = 0;
    int pawn_move = 1;
    const char *castle_rights = "KQkq";
    const char *en_passant = "-";
    
    if (!PyArg_ParseTuple(args, "O|ssis", &board, &pos, &move, &pawn_move, &castle_rights, &en_passant)) {
        return NULL;
    }

    vector<string> pos_part;
    string position(pos);
    stringstream ss(position);
    string temp;
    while (ss >> temp) {
        pos_part.push_back(temp);
    }
    if (move) {
        pos_part[1] = (pos_part[1] == "w") ? "b" : "w";
        pos_part[2] = castle_rights;
        pos_part[3] = en_passant;
        pos_part[4] = (pawn_move) ? "0" : to_string(stoi(pos_part[4]) + 1);
        pos_part[5] = (pos_part[1] == "w") ? pos_part[5] : to_string(stoi(pos_part[5]) + 1);
    }
    string pos_part_str = " ";
    for (size_t i = 1; i < pos_part.size(); ++i) {
        pos_part_str += pos_part[i] + " ";
    }
    pos_part_str = pos_part_str.substr(0, pos_part_str.size() - 1);

    vector<string> fen_rows;
    Py_ssize_t num_rows = PyList_Size(board);
    for (Py_ssize_t i = 0; i < num_rows; ++i) {
        PyObject *row = PyList_GetItem(board, i);
        string fen_row = "";
        int empty_count = 0;
        
        Py_ssize_t num_cols = PyList_Size(row);
        for (Py_ssize_t j = 0; j < num_cols; ++j) {
            PyObject *cell = PyList_GetItem(row, j);
            const char *cell_str = PyUnicode_AsUTF8(cell);
            if (strcmp(cell_str, "0") == 0) {
                empty_count++;
            } else {
                if (empty_count > 0) {
                    fen_row += to_string(empty_count);
                    empty_count = 0;
                }
                fen_row += cell_str;
            }
        }
        if (empty_count > 0) {
            fen_row += to_string(empty_count);
        }
        fen_rows.push_back(fen_row);
    }

    string fen_position = "";
    for (size_t i = 0; i < fen_rows.size(); ++i) {
        fen_position += fen_rows[i] + "/";
    }
    fen_position = fen_position.substr(0, fen_position.size() - 1);

    return PyUnicode_FromString((fen_position + pos_part_str).c_str());
}

static PyObject *
get_color(PyObject *self, PyObject *args) {
    const char *piece;
    if (!PyArg_ParseTuple(args, "s", &piece)) {
        return NULL;
    }
    
    if (isupper(piece[0])) {
        Py_INCREF(Py_True);
        return Py_True;
    } else if (islower(piece[0])) {
        Py_INCREF(Py_False);
        return Py_False;
    } else {
        Py_INCREF(Py_None);
        Py_RETURN_NONE;
    }
}

static PyMethodDef ChessMethods[] = {
    {"FEN_to_board", FEN_to_board, METH_VARARGS, 
    "Convert FEN string to board array"},
    {"board_to_FEN", board_to_FEN, METH_VARARGS, 
    "Convert board array to FEN string"},
    {"get_color", get_color, METH_VARARGS,
    "Get color of piece"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef chessmodule = {
    PyModuleDef_HEAD_INIT,
    "chess",
    NULL,
    -1,
    ChessMethods
};

PyMODINIT_FUNC PyInit_chess(void) {
    PyObject *m;

    m = PyModule_Create(&chessmodule);
    if (m == NULL)
        return NULL;

    ChessError = PyErr_NewException("chess.error", NULL, NULL);
    Py_XINCREF(ChessError);
    if (PyModule_AddObject(m, "error", ChessError) < 0) {
        Py_XDECREF(ChessError);
        Py_CLEAR(ChessError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

int main(int argc, char *argv[]) {
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    if (PyImport_AppendInittab("chess", PyInit_chess) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    Py_SetProgramName(program);
    Py_Initialize();

    PyObject *pmodule = PyImport_ImportModule("chess");
    
    if (!pmodule) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'chess'\n");
    }

    PyMem_RawFree(program);
    return 0;
}
