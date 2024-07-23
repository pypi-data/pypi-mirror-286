# cpp_protein_encoders

To use them as input to an ML model, protein sequences have to
be encoded (e.g. one-hot encoding, etc.) It's *very* easy to write
Python code to do this, but if you do this often enough, at some point
you'll realize you have multiple redundant code blocks in different
projects that all do the same thing. For this reason, it's convenient
to have a single simple plugin tool to do basic protein encoding wherever
you need it. `cpp_protein_encoders` provides a simple,
fast and flexible tool for common encoding schemes (I'll add
more over time if I find any others I am using frequently -- please
feel free to suggest any that you would find useful.)

Currently supported schemes include:

- One-hot encoding with either a 2d or 3d array as output, using either the
basic 20 amino acid alphabet, or the basic alphabet plus gaps, or an extended
alphabet including unusual symbols (B, J, O, U, X, Z).
- Integer encoding, using either the basic 20 amino acid alphabet, or the basic alphabet plus gaps, or an extended
alphabet including unusual symbols (B, J, O, U, X, Z). Integer encoding is
useful for LightGBM (gradient boosted trees) and some clustering schemes.
- Substitution matrix encoding using a 21 letter alphabet (standard AAs plus
gaps) with various percent homologies and two encoding schemes supported.

`cpp_protein_encoders` encodes sequences as numpy arrays. Why not as
PyTorch / Jax / Tensorflow? There are two reasons for this. First, numpy is
much more universal. A numpy array is easily converted to e.g. a PyTorch
(or other framework) array in-place with negligible overhead. Moreover,
you may need to use encoded sequences as input to a library like LightGBM,
XGBoost or xGPR that takes numpy arrays as input.

Second, by using numpy we ensure this package has only a single
dependency -- numpy -- which is *relatively* lightweight (the same cannot
be said for PyTorch or Tensorflow).

Since this package is (at this time) small and simple,
documentation is relatively brief and is below.

### Performance

Sequence encoding is almost never the bottleneck in ML or statistical
analysis (if it is, you're doing something unusual). Still, FWIW, this
package gives roughly an order of magnitude speed improvement over a
naive pure Python approach (more if you are processing numerous
minibatches).

### Installation
```
pip install cpp_protein_encoders
```

### Usage

```python
from cpp_protein_encoders import OneHotProteinEncoder, IntegerProteinEncoder
from cpp_protein_encoders import SubstitutionMatrixEncoder

# Note that all characters are expected to be uppercase.

sequences = ['AAAGGGYYY', 'CCCTTTAAA', 'GGGTTTFF-']
```

When creating a OneHotProteinEncoder or an IntegerProteinEncoder, we
can use either the 'standard' alphabet (basic 20 AAs), the 'gapped'
alphabet (basic 20 AAs + gaps), or the 'expanded' alphabet (gaps +
unusual AAs, see above). If we pass sequences that contain unexpected
characters, an exception will be raised.

```python
encoder1 = OneHotProteinEncoder(alphabet = 'gapped')
encoder2 = IntegerProteinEncoder(alphabet = 'gapped')
```

For substitution matrices, we can select a homology value to indicate
which substitution matrix to use (90% homology, 85%, and so on).
Current options are '95', '90', '85', '75', '62'.
We can also set 'use_standardized_mat' to be True or False. If True,
each AA is encoded using the corresponding row of a scaled Cholesky
decomposition of a distance matrix built using the substitution matrix.
This ensures that the Euclidean distance between any two representations
is equal to the distance between them as determined using the substitution
matrix. This can work well for kernel machines and some NNs. Alternatively,
we can set 'use_standardized_mat' to be False, in which case the AAs are
encoded as the corresponding row of the substitution matrix. This is
unlikely to work well in kernel machines but may work well for some NNs.

```python
encoder3 = SubstitutionMatrixEncoder(homology = '90', use_standardized_mat = True)
```

When encoding, there are two important options:
`max_length` and `flatten_output_array`. `max_length` can be None or
an integer. If None, the maximum length is determined from the input
sequence list and all sequences are if necessary zero-padded to be that
length. If `max_length` is an int, all sequences are if necessary zero-
padded to be `max_length`. (If you specify max length then pass a sequence
that is *longer*, an exception will be raised).

The output array is normally a 3d array of size N x M x A for N sequences,
M amino acids and A alphabet size. If `flatten_output_array` is True,
this is flattened to a 2d array of size N x (M * A). *IMPORTANT*: For
integer encoding, the output array is always a 2d array anyway, so
`flatten_output_array` is not in that case accepted as an option.

```python
first_set = encoder1.encode(sequences, flatten_output_array = False, max_length = None)
second_set = encoder2.encode(sequences, max_length = None)
third_set = encoder3.encode(sequences, flatten_output_array = False, max_length = None)
```
