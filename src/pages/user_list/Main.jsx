import React, { useEffect, useState, useCallback } from "react";
import useFetch from "../../hook/getData";
import { FaEdit, FaTrash } from "react-icons/fa";
import useDelete from "../../hook/delete";
import ReusableTable from "../../hook/TableHook";
import FormModal from "../../hook/FormModal";

const UserList = () => {
  const [usersData, setUsersData] = useState([]);
  const [createUserModal, setCreateUserModal] = useState(false);
  const [updateUserModal, setUpdateUserModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const { data: users, loading, error } = useFetch("/auth/user/list/");
  const { handleDelete } = useDelete("/auth/user/list/");

  // Populate usersData when fetch succeeds
  useEffect(() => {
    if (users) setUsersData(users);
  }, [users]);

  // Handle create user
  const handleCreated = useCallback((newUser) => {
    setUsersData((prev) => [...prev, newUser]);
    setCreateUserModal(false);
  }, []);

  // Handle update user
  const handleUserUpdated = useCallback((updatedUser) => {
    setUsersData((prev) =>
      prev.map((user) => (user.id === updatedUser.id ? updatedUser : user))
    );
    setUpdateUserModal(false);
  }, []);

  // Handle edit button click
  const handleEdit = useCallback((user) => {
    setSelectedUser(user);
    setUpdateUserModal(true);
  }, []);

  // Handle delete button click
  const handleDeleteUser = useCallback(
    async (userId) => {
      if (!window.confirm("Are you sure you want to delete this user?")) return;

      try {
        await handleDelete(userId);
        setUsersData((prev) => prev.filter((user) => user.id !== userId));
      } catch {
        alert("Failed to delete user. Please try again.");
      }
    },
    [handleDelete]
  );

  if (loading) return <p className="p-6">Loading...</p>;
  if (error) return <p className="p-6 text-red-500">{error}</p>;

  // Table columns
  const columns = [
    { header: "SL No", render: (row, index) => <p className="text-center">{index + 1}</p> },
    { header: "Full Name", accessor: "full_name" },
    { header: "Email", accessor: "email" },
    { header: "Phone Number", accessor: "phone_number" },
    { header: "Active", accessor: "is_active", render: (row) => (row.is_active ? "Yes" : "No") },
  ];

  // Actions
  const actions = [
    {
      label: "Edit",
      icon: <FaEdit />,
      className: "text-blue-500 hover:underline",
      onClick: (row) => handleEdit(row),
    },
    {
      label: "Delete",
      icon: <FaTrash />,
      className: "text-red-500 hover:underline",
      onClick: (row) => handleDeleteUser(row.id),
    },
  ];

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold ps-5 text-gray-500">Users List</h2>
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          onClick={() => setCreateUserModal(true)}
        >
          Create User
        </button>
      </div>

      {/* Table */}
      <ReusableTable columns={columns} data={usersData} actions={actions} />

      {/* Create User Modal */}
      <FormModal
        isOpen={createUserModal}
        onClose={() => setCreateUserModal(false)}
        onSuccess={handleCreated}
        endpoint="/auth/user/list/"
        title="Create User"
        fields={[
          { name: "full_name", label: "Full Name", type: "text", placeholder: "Enter full name", required: true },
          { name: "email", label: "Email", type: "email", placeholder: "Enter email", required: true },
          { name: "phone_number", label: "Phone Number", type: "text", placeholder: "Enter phone number", required: false },
          { name: "is_active", label: "Active", type: "boolean", required: true },
        ]}
        mode="create"
      />

      {/* Update User Modal */}
      {selectedUser?.id && (
        <FormModal
          isOpen={updateUserModal}
          onClose={() => setUpdateUserModal(false)}
          onSuccess={handleUserUpdated}
          endpoint={`/auth/user/list/${selectedUser.id}/`}
          title="Update User"
          data={selectedUser}
          fields={[
            { name: "full_name", label: "Full Name", type: "text", placeholder: "Enter full name", required: true },
            { name: "email", label: "Email", type: "email", placeholder: "Enter email", required: true },
            { name: "phone_number", label: "Phone Number", type: "text", placeholder: "Enter phone number", required: false },
            { name: "is_active", label: "Active", type: "boolean", required: true },
          ]}
          mode="update"
        />
      )}
    </div>
  );
};

export default UserList;
