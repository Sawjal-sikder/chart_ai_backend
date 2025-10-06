import React, { useState, useEffect } from "react";
import useApiMutation from "../../hook/Create";

const CreateCityModal = ({ isOpen, onClose, onCityCreated }) => {
      const { createData, loading, error, success } = useApiMutation("/services/cities/");
      const [formData, setFormData] = useState({
            name: "",
            description: "",
      });

      // Reset form and success message when modal opens
      useEffect(() => {
            if (isOpen) {
                  setFormData({ name: "", description: "" });
            }
      }, [isOpen]);

      if (!isOpen) return null;

      const handleChange = (e) => {
            setFormData({ ...formData, [e.target.name]: e.target.value });
      };

      const handleSubmit = async (e) => {
            e.preventDefault();
            try {
                  const data = await createData(formData); // Call the hook
                  console.log("Created City:", data);
                  onClose(); // close modal after successful creation
                  if (onCityCreated) onCityCreated(data);
            } catch (err) {
                  console.error("Error creating city:", err);
            }
      };

      return (
            <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
                  {/* Modal box */}
                  <div className="bg-white rounded-lg shadow-lg w-full max-w-lg p-6">
                        <h2 className="text-2xl text-center text-gray-600 font-semibold mb-6">Create City</h2>

                        {/* Feedback messages */}
                        {loading && <p className="text-blue-600 mb-2">Creating city...</p>}
                        {error && <p className="text-red-600 mb-2">{JSON.stringify(error)}</p>}
                        {success && <p className="text-green-600 mb-2">City created successfully!</p>}

                        {/* Form */}
                        <form onSubmit={handleSubmit} className="space-y-5">
                              <div>
                                    <label className="block text-sm font-medium">City Name</label>
                                    <input
                                          type="text"
                                          name="name"
                                          value={formData.name}
                                          onChange={handleChange}
                                          className="mt-1 w-full border rounded px-3 py-4 focus:ring focus:ring-blue-300"
                                          placeholder="Enter city name"
                                          required
                                    />
                              </div>

                              <div>
                                    <label className="block text-sm font-medium">Description</label>
                                    <textarea
                                          name="description"
                                          value={formData.description}
                                          onChange={handleChange}
                                          rows={5}
                                          className="mt-1 w-full border rounded px-3 py-4 focus:ring focus:ring-blue-300"
                                          placeholder="Enter description"
                                    />
                              </div>

                              {/* Buttons */}
                              <div className="flex justify-end gap-3 mt-4">
                                    <button
                                          type="button"
                                          onClick={onClose}
                                          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                                    >
                                          Cancel
                                    </button>
                                    <button
                                          type="submit"
                                          disabled={loading}
                                          className={`px-4 py-2 text-white rounded ${loading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"}`}
                                    >
                                          {loading ? "Saving..." : "Save"}
                                    </button>
                              </div>
                        </form>
                  </div>
            </div>
      );
};

export default CreateCityModal;
