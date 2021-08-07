import tensorflow as tf

print(tf.version)

rank0_string = tf.Variable("this is a string",tf.string)
rank0_number = tf.Variable(5,tf.int16)
rank0_floating = tf.Variable(5.67,tf.float64)

print(rank0_string)
print(rank0_number)
print(rank0_floating)

print("\n")

rank1_string = tf.Variable(["test","test1"],tf.string)
rank2_string = tf.Variable([["test","test1","test2"],["test","hallo","hugo"]],tf.string)

print(rank1_string)
print(rank2_string)

print(tf.rank(rank0_string))
print(tf.rank(rank1_string))
print(tf.rank(rank2_string))

print(tf.shape(rank0_string))
print(tf.shape(rank1_string))
print(tf.shape(rank2_string))

print("\n")

t0 = tf.ones([1,2,3])
t1 = tf.reshape(t0, [2,3,1])
t2 = tf.reshape(t0, [3, -1])    #-1 is wild card

print(t0)
print(t1)
print(t2)

print("\n")