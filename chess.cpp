#include <Python.h>
#include <vector>
#include <string>
#include <sstream>

static PyObject *ChessError;

static PyObject *
FEN_to_board_test(PyObject *self, PyObject *args) {
    const char *pos;
    if (!PyArg_ParseTuple(args, "s", &pos)) {
        return NULL;
    }

    PyObject *board = PyList_New(8);
    short currCol = 0;

    PyObject* board_row = PyList_New(8);
    short lastInRow = 0;

    while(true) {
        if(*pos & 0x40) {
            PyList_SetItem(board_row, lastInRow++, PyUnicode_FromStringAndSize(pos, 1));
        } 
        else if (*pos & 0x20 && *pos & 0x10) {
            for (short j = 0; j < *pos - '0'; j++) {
                PyList_SetItem(board_row, lastInRow++, PyUnicode_FromString("0"));
            }
        }
        else {
            PyList_SetItem(board, currCol++, board_row);
            lastInRow = 0;
            board_row = PyList_New(8);
            if(!(*pos & 0xF)) break;
        }

        pos++;
    }

    return board;
}

static PyObject *
FEN_to_board(PyObject *self, PyObject *args) {
    const char *pos;
    if (!PyArg_ParseTuple(args, "s", &pos)) {
        return NULL;
    }

    PyObject *board = PyList_New(8);
    short currCol = 0;

    PyObject* board_row = PyList_New(8);
    short lastInRow = 0;

    while(1) {
        if (*pos >= '1' && *pos <= '8') {
            for (short j = 0; j < *pos - '0'; j++) {
                PyList_SetItem(board_row, lastInRow++, PyUnicode_FromString("0"));
            }
        }
        else if (*pos == '/' || *pos == ' ') {
            PyList_SetItem(board, currCol++, board_row);
            lastInRow = 0;
            board_row = PyList_New(8);
            if(*pos == ' ') break;
        } 
        else {
            PyList_SetItem(board_row, lastInRow++, PyUnicode_FromStringAndSize(pos, 1));
        }

        pos++;
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

    std::vector<std::string> pos_part;
    std::string position(pos);
    std::stringstream ss(position);
    std::string temp;
    while (ss >> temp) {
        pos_part.push_back(temp);
    }
    if (move) {
        pos_part[1] = (pos_part[1] == "w") ? "b" : "w";
        pos_part[2] = castle_rights;
        pos_part[3] = en_passant;
        pos_part[4] = (pawn_move) ? "0" : std::to_string(std::stoi(pos_part[4]) + 1);
        pos_part[5] = (pos_part[1] == "w") ? pos_part[5] : std::to_string(std::stoi(pos_part[5]) + 1);
    }
    std::string pos_part_str = " ";
    for (size_t i = 1; i < pos_part.size(); ++i) {
        pos_part_str += pos_part[i] + " ";
    }
    pos_part_str = pos_part_str.substr(0, pos_part_str.size() - 1);

    std::vector<std::string> fen_rows;
    Py_ssize_t num_rows = PyList_Size(board);
    for (Py_ssize_t i = 0; i < num_rows; ++i) {
        PyObject *row = PyList_GetItem(board, i);
        std::string fen_row = "";
        int empty_count = 0;
        
        Py_ssize_t num_cols = PyList_Size(row);
        for (Py_ssize_t j = 0; j < num_cols; ++j) {
            PyObject *cell = PyList_GetItem(row, j);
            const char *cell_str = PyUnicode_AsUTF8(cell);
            if (strcmp(cell_str, "0") == 0) {
                empty_count++;
            } else {
                if (empty_count > 0) {
                    fen_row += std::to_string(empty_count);
                    empty_count = 0;
                }
                fen_row += cell_str;
            }
        }
        if (empty_count > 0) {
            fen_row += std::to_string(empty_count);
        }
        fen_rows.push_back(fen_row);
    }

    std::string fen_position = "";
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
    {"FEN_to_board_test", FEN_to_board_test, METH_VARARGS,
    "Convert FEN string to board array"},
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
