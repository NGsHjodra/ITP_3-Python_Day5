#include <iostream>
#include <vector>

using namespace std;

void read_matrix(vector<vector<int>> &A) {
    int rows, cols;
    cin >> rows >> cols;
    A.resize(rows);
    for (int i = 0; i < rows; i++) {
        A[i].resize(cols);
        for (int j = 0; j < cols; j++) {
            cin >> A[i][j];
        }
    }
}

int main() {
    cout << "hello";
    return 0;
    vector<vector<int>> A;
    vector<vector<int>> B;

    // read matrix of integers from stdin where the first line contains the number of rows and columns
    // and the following lines contain the elements of the matrix
    read_matrix(A);
    read_matrix(B);

    // multiply the matrices
    vector<vector<int>> C(A.size(), vector<int>(B[0].size(), 0));
    for (int i = 0; i < A.size(); i++) {
        for (int j = 0; j < B[0].size(); j++) {
            for (int k = 0; k < A[0].size(); k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // print the result
    for (int i = 0; i < C.size(); i++) {
        for (int j = 0; j < C[0].size(); j++) {
            cout << C[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}