import sys


# Class for heap nodes
class Heap_Node:
    def __init__(self, ride, rbt, min_heap_index):
        # a Heap_Node object stores a ride object, a red-black tree object, and the index of the node in the min heap
        self.ride = ride
        self.rbTree = rbt
        self.min_heap_index = min_heap_index


# Class for Minheap
class Min_Heap:
    def __init__(self):
        # initialize an empty heap list with a dummy element at index 0, and set the current size to 0
        self.heap_list = [0]
        self.current_size = 0

    def insert(self, element):
        # add an element to the end of the heap list and increment the current size
        self.heap_list.append(element)
        self.current_size += 1
        # perform bottom-up heapify to maintain the min heap property
        self.fix_heap_bottom_up(self.current_size)

    def fix_heap_bottom_up(self, heap_element_index):
        # starting from the given node index heap_element_index, swap the node with its parent if its key is less than
        # its parent's key, and repeat the process until the node's key is greater than or equal to its parent's key
        while (heap_element_index // 2) > 0:
            if self.heap_list[heap_element_index].ride.is_less_than(self.heap_list[heap_element_index // 2].ride):
                self.swap(heap_element_index, (heap_element_index // 2))
            else:
                break
            heap_element_index = heap_element_index // 2

    def swap(self, index1, index2):
        self.heap_list[index1], self.heap_list[index2] = self.heap_list[index2], self.heap_list[index1]
        self.heap_list[index1].min_heap_index, self.heap_list[index2].min_heap_index = index1, index2

    def fix_heap_top_down(self, heap_element_index):
        # starting from the given node index heap_element_index, repeatedly swap it with its minimum child until it
        # is less than both of its children, or until it reaches a leaf node
        while (heap_element_index * 2) <= self.current_size:
            ind = self.get_min_child_index(heap_element_index)
            if not self.heap_list[heap_element_index].ride.is_less_than(self.heap_list[ind].ride):
                self.swap(heap_element_index, ind)
            heap_element_index = ind

    def get_min_child_index(self, heap_element_index):
        # return the index of the minimum child of the node at the given index heap_element_index
        if (heap_element_index * 2) + 1 > self.current_size:
            return heap_element_index * 2
        else:
            if self.heap_list[heap_element_index * 2].ride.is_less_than(
                    self.heap_list[(heap_element_index * 2) + 1].ride):
                return heap_element_index * 2
            else:
                return (heap_element_index * 2) + 1

    def update_element(self, heap_element_index, new_key):
        # update the key of the node at the given index heap_element_index to the given new_key, and perform either
        # bottom-up or top-down heapify depending on whether the node's key is now less than or greater than its
        # parent's key
        node = self.heap_list[heap_element_index]
        node.ride.tripDuration = new_key
        if heap_element_index == 1:
            self.fix_heap_top_down(heap_element_index)
        elif self.heap_list[heap_element_index // 2].ride.is_less_than(self.heap_list[heap_element_index].ride):
            self.fix_heap_top_down(heap_element_index)
        else:
            self.fix_heap_bottom_up(heap_element_index)

    def delete_element(self, heap_element_index):
        # Replace element with last element in heap and remove last element
        self.swap(heap_element_index, self.current_size)
        self.current_size -= 1
        *self.heap_list, _ = self.heap_list
        # Fix heap property
        self.fix_heap_top_down(heap_element_index)

    def pop_top_element(self):
        # Return 'No Rides Available' if heap is empty
        if len(self.heap_list) == 1:
            return 'No Rides Available'
        # Get root element and replace with last element in heap, then remove last element
        root = self.heap_list[1]
        self.swap(1, self.current_size)
        self.current_size -= 1
        *self.heap_list, _ = self.heap_list
        # Fix heap property
        self.fix_heap_top_down(1)
        return root


# Class to represent a node in Red-Black Tree
class RedBlackTreeNode:
    def __init__(self, ride, min_heap_node):
        # The ride object stored in the node
        self.ride = ride

        # Parent node of this node
        self.parent = None

        # Left child node
        self.left = None

        # Right child node
        self.right = None

        # Color of the node (1 = RED, 0 = BLACK)
        self.color = 1

        # Reference to the corresponding node in the min heap
        self.min_heap_node = min_heap_node


# Class for red black tree
class Red_Black_Tree:
    def __init__(self):
        # Creating null node and setting its attributes
        self.null_node = RedBlackTreeNode(None, None)
        self.null_node.left = None
        self.null_node.right = None
        self.null_node.color = 0  # Black color
        self.root = self.null_node

    # To retrieve the ride with the rideNumber equal to the key
    def get_ride(self, key):
        temp = self.root

        # Iterating through the tree to find the node with rideNumber equal to the key
        while temp != self.null_node:
            if temp.ride.rideNumber == key:
                return temp
            if temp.ride.rideNumber < key:
                temp = temp.right
            else:
                temp = temp.left

        return None

    # This method returns a list of rides within a certain price range
    # It calls the recursive helper function find_rides_in_range
    # that traverses the tree and adds the relevant rides to the result list
    def get_rides_in_range(self, low, high):
        result = []
        self.find_rides_in_range(self.root, low, high, result)
        return result

    def find_rides_in_range(self, node, low, high, result):
        if node == self.null_node:
            return
        if low < node.ride.rideNumber:
            self.find_rides_in_range(node.left, low, high, result)
        if low <= node.ride.rideNumber <= high:
            result.append(node.ride)
        self.find_rides_in_range(node.right, low, high, result)

    # This method returns the minimum node in the tree
    # It traverses the left child of each node until it finds a leaf node
    def get_minimum(self, node):
        while node.left != self.null_node:
            node = node.left
        return node

    # This method performs a left rotation around a given node x
    # It updates the parent and child relationships of x and y
    # to maintain the RBT property
    def left_rotation(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.null_node:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # This method performs a right rotation around a given node x
    # It updates the parent and child relationships of x and y
    # to maintain the RBT property
    def right_rotation(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.null_node:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # This method replaces a node with its child node in a Red-Black Tree (RBT).
    def __replace_node(self, node, child_node):

        # If the node to be replaced is the root node of the tree, then set the child node as the new root.
        if node.parent is None:
            self.root = child_node
        # If the node to be replaced is the right child of its parent, then set the child node as the new right child.
        elif node == node.parent.right:
            node.parent.right = child_node
        # If the node to be replaced is the left child of its parent, then set the child node as the new left child.
        else:
            node.parent.left = child_node
        # Set the parent of the child node as the parent of the node to be replaced.
        child_node.parent = node.parent

    def insert(self, ride, min_heap):
        # create a new node with the given ride and min_heap
        node = RedBlackTreeNode(ride, min_heap)

        # set initial node attributes and color to red
        node.parent = None
        node.left = self.null_node
        node.right = self.null_node
        node.color = 1

        # traverse through the tree to find the proper position for the new node
        insertion_node = None
        temp_node = self.root
        while temp_node != self.null_node:
            insertion_node = temp_node
            if node.ride.rideNumber < temp_node.ride.rideNumber:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right

        # set the parent and children of the new node
        node.parent = insertion_node
        if insertion_node is None:
            self.root = node
        elif node.ride.rideNumber > insertion_node.ride.rideNumber:
            insertion_node.right = node
        else:
            insertion_node.left = node

        # balance the tree after insertion
        if node.parent is None:
            # if the new node is the root node, color it black
            node.color = 0
            return
        if node.parent.parent is None:
            # if the new node is a child of the root node, no need to balance
            return
        self.insert_balance(node)

    # Balances the tree after inserting a node
    def insert_balance(self, curr_node):

        # Perform rotations and recoloring to balance the tree
        while curr_node.parent.color == 1:
            if curr_node.parent == curr_node.parent.parent.left:
                parent_sibling = curr_node.parent.parent.right
                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.right:
                        curr_node = curr_node.parent
                        self.left_rotation(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.right_rotation(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent
            else:
                parent_sibling = curr_node.parent.parent.left
                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.left:
                        curr_node = curr_node.parent
                        self.right_rotation(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.left_rotation(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent
            if curr_node == self.root:
                break
        self.root.color = 0

    def delete_node(self, rideNumber):
        # call the helper function to delete the node with the given ride number
        return self.delete_helper(self.root, rideNumber)

    # Deletes a node from the tree and returns the corresponding heap node
    def delete_helper(self, node, key):

        # Traverse the tree to find the node to delete
        delete_node = self.null_node
        while node != self.null_node:
            if node.ride.rideNumber == key:
                delete_node = node
            if node.ride.rideNumber >= key:
                node = node.left
            else:
                node = node.right

        # If node to delete is not found, return
        if delete_node == self.null_node:
            return

        # Store information about the node to be deleted
        heap_node = delete_node.min_heap_node
        y = delete_node
        y_original_color = y.color

        # Handle case where node has at most one child
        if delete_node.left == self.null_node:
            x = delete_node.right
            self.__replace_node(delete_node, delete_node.right)
        elif (delete_node.right == self.null_node):
            x = delete_node.left
            self.__replace_node(delete_node, delete_node.left)

        # Handle case where node has two children
        else:
            y = self.get_minimum(delete_node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == delete_node:
                x.parent = y
            else:
                self.__replace_node(y, y.right)
                y.right = delete_node.right
                y.right.parent = y
            self.__replace_node(delete_node, y)
            y.left = delete_node.left
            y.left.parent = y
            y.color = delete_node.color

        # Balance the tree after deleting the node
        if y_original_color == 0:
            self.delete_balance(x)
        return heap_node

    # Method to balance the tree after deletion
    def delete_balance(self, node):
        # Loop until node reaches the root node and its color is black
        while node != self.root and node.color == 0:
            if node == node.parent.right:
                # Case 1: Node is on the right side of its parent
                parent_sibling = node.parent.left
                if parent_sibling.color != 0:
                    # Case 1.1: The sibling node is red
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.right_rotation(node.parent)
                    parent_sibling = node.parent.left

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    # Case 1.2: Both children of sibling node are black
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.left.color != 1:
                        # Case 1.3: Left child of sibling node is red
                        parent_sibling.right.color = 0
                        parent_sibling.color = 1
                        self.left_rotation(parent_sibling)
                        parent_sibling = node.parent.left

                    # Case 1.4: Right child of sibling node is red
                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.left.color = 0
                    self.right_rotation(node.parent)
                    node = self.root
            else:
                # Case 2: Node is on the left side of its parent
                parent_sibling = node.parent.right
                if parent_sibling.color != 0:
                    # Case 2.1: The sibling node is red
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.left_rotation(node.parent)
                    parent_sibling = node.parent.right

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    # Case 2.2: Both children of sibling node are black
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.right.color != 1:
                        # Case 2.3: Right child of sibling node is red
                        parent_sibling.left.color = 0
                        parent_sibling.color = 1
                        self.right_rotation(parent_sibling)
                        parent_sibling = node.parent.right

                    # Case 2.4: Left child of sibling node is red
                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.right.color = 0
                    self.left_rotation(node.parent)
                    node = self.root

        # Setting the color of the final node to black
        node.color = 0


class Ride:
    def __init__(self, rideNumber, rideCost, tripDuration):
        # initialize a new Ride object with the given rideNumber, rideCost, and tripDuration
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration

    def is_less_than(self, other_ride):
        # compare two Ride objects and determine which one is less than the other based on cost and duration
        if self.rideCost == other_ride.rideCost:
            if self.tripDuration > other_ride.tripDuration:
                return False
            else:
                return True
        elif self.rideCost < other_ride.rideCost:
            return True
        elif self.rideCost > other_ride.rideCost:
            return False


# Function to insert a new ride into the system
def insert_ride(ride, heap, rbt):
    # Check if the ride number already exists in the system
    if rbt.get_ride(ride.rideNumber) is not None:
        output_helper(None, "Duplicate RideNumber", False)
        # If ride number already exists, exit the program
        sys.exit(0)
        return
    # Create a new Red-Black Tree node and a corresponding Min Heap node
    rbt_node = RedBlackTreeNode(None, None)
    min_heap_node = Heap_Node(ride, rbt_node, heap.current_size + 1)
    # Insert the new nodes into both the heap and the Red-Black Tree
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)


# Function to get the next ride request from the system
def get_next_ride(heap, rbt):
    # Check if there are any active ride requests in the system
    if heap.current_size != 0:
        # Pop the top ride request from the Min Heap and delete its corresponding node from the Red-Black Tree
        popped_node = heap.pop_top_element()
        rbt.delete_node(popped_node.ride.rideNumber)
        output_helper(popped_node.ride, "", False)
    else:
        output_helper(None, "No active ride requests", False)


# Function to cancel a ride request from the system
def cancel_ride(ride_number, heap, rbt):
    # Delete the ride request from the Red-Black Tree and get its corresponding Min Heap node
    heap_node = rbt.delete_node(ride_number)
    if heap_node is not None:
        # Delete the corresponding Min Heap node
        heap.delete_element(heap_node.min_heap_index)


# Function to update the duration of a ride request in the system
def update_ride(rideNumber, new_duration, heap, rbt):
    # Get the Red-Black Tree node corresponding to the ride request
    rbt_node = rbt.get_ride(rideNumber)
    if rbt_node is None:
        # If ride request doesn't exist, print a message indicating the same
        print("")
    elif new_duration <= rbt_node.ride.tripDuration:
        # If the new duration is less than or equal to the current duration, update the Min Heap node accordingly
        heap.update_element(rbt_node.min_heap_node.min_heap_index, new_duration)
    elif rbt_node.ride.tripDuration < new_duration <= (2 * rbt_node.ride.tripDuration):
        # If the new duration is between the current duration and twice the current duration, cancel the ride request
        # and insert a new ride request with the updated duration and cost
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)
        insert_ride(Ride(rbt_node.ride.rideNumber, rbt_node.ride.rideCost + 10, new_duration), heap, rbt)
    else:
        # If the new duration is more than twice the current duration, cancel the ride request
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)


def print_ride(rideNumber, rbt):
    # get the ride from the red-black tree using the given ride number
    result = rbt.get_ride(rideNumber)
    # if the result is None, i.e. no ride was found with the given ride number
    if result is None:
        # add a placeholder ride with all values set to 0 to the output
        output_helper(Ride(0, 0, 0), "", False)
    else:
        # add the found ride to the output
        output_helper(result.ride, "", False)


def print_rides(low, high, rbt):
    # get a list of rides from the red-black tree within the given range [low, high]
    list = rbt.get_rides_in_range(low, high)
    # add the list of rides to the output as a single string, with each ride separated by a newline character
    output_helper(list, "", True)


def output_helper(ride, message, list):
    file = open("output_file.txt", "a")
    if ride is None:
        file.write(message + "\n")
    else:
        message = ""
        if not list:
            message += ("(" + str(ride.rideNumber) + "," + str(ride.rideCost) + "," + str(ride.tripDuration) + ")\n")
        else:
            if len(ride) == 0:
                message += "(0,0,0)\n"
            for i in range(len(ride)):
                if i != len(ride) - 1:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + "),")
                else:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + ")\n")

        file.write(message)
    file.close()


# The main function
def main():
    # Check if the number of arguments provided is valid
    if len(sys.argv) < 2:
        print("Invalid Arguments")
        print("Enter Command of the form : python3 gator_taxi.py <input_file_name.txt>")
        return

    # Create a heap and a red-black tree to store the rides
    ride_heap = Min_Heap()
    ride_tree = Red_Black_Tree()

    # Open the input and output files
    with open(sys.argv[1], "r") as input_file, open("output_file.txt", "w") as output_file:

        # Read each line of the input file
        for line in input_file.readlines():

            # Extract the ride details from the line
            ride_details = [int(i) for i in line[line.index("(") + 1:line.index(")")].split(",") if i != '']

            # Depending on the command, either insert, update, get next, cancel, or print the ride/range of rides
            if "Insert" in line:  # Insert a new ride
                ride = Ride(ride_details[0], ride_details[1], ride_details[2])
                insert_ride(ride, ride_heap, ride_tree)
            elif "UpdateTrip" in line:  # Update trip
                update_ride(ride_details[0], ride_details[1], ride_heap, ride_tree)
            elif "GetNextRide" in line:  # Get the Next Ride
                get_next_ride(ride_heap, ride_tree)
            elif "CancelRide" in line:  # Cancel Ride
                cancel_ride(ride_details[0], ride_heap, ride_tree)
            elif "Print" in line:
                if len(ride_details) == 1:  # Print one Specific Ride
                    print_ride(ride_details[0], ride_tree)
                elif len(ride_details) == 2:  # Print Range of Rides
                    print_rides(ride_details[0], ride_details[1], ride_tree)

    # Close the output file
    output_file.close()


# Call the main function after the file is run
if __name__ == "__main__":
    main()