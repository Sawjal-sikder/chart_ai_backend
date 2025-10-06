import React, { useState, useEffect } from "react";
import useUpdate from "../../hook/update";

const UpdateCityModal = ({ isOpen, onClose, onCityUpdated, city }) => {
      const { data, loading, error, updateData } = useUpdate("/services/cities/");
      const [formData, setFormData] = useState({
            name: "",
            description: "",
      });


      useEffect(() => {
            if (city && city.id) {
                  // console.log("Setting form data for city:", city);
                  setFormData({
                        name: city.name || "",
                        description: city.description || "",
                  });
            }
      }, [city]);

      // Handle form input changes
      const handleChange = (e) => {
            const { name, value } = e.target;
            setFormData(prev => ({
                  ...prev,
                  [name]: value
            }));
      };

      const handleSubmit = async (e) => {
            e.preventDefault();

            // Check if city and city.id exist
            if (!city || !city.id) {
                  // console.error("City or city.id is missing:", city);
                  alert("Error: City data is missing. Please try again.");
                  return;
            }

            // console.log("Submitting update for city ID:", city.id);
            // console.log("Form data:", formData);

            try {
                  const updated = await updateData(`/services/cities/${city.id}/`, formData);
                  // console.log("Updated data:", updated);
                  onCityUpdated(updated);
                  onClose();
            } catch (err) {
                  // console.error("Update error:", err);
                  alert("Failed to update city. Please try again.");
            }
      };

      // Don't render if modal is not open
      if (!isOpen) return null;

      return (
            <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
                  {/* Modal box */}
                  <div className="bg-white rounded-lg shadow-lg w-full max-w-lg p-6">
                        <h2 className="text-2xl text-center text-gray-600 font-semibold mb-6">
                              Update City
                        </h2>



                        {/* Feedback messages */}
                        {loading && <p className="text-blue-600 mb-2">Updating city...</p>}
                        {error && <p className="text-red-600 mb-2">{JSON.stringify(error)}</p>}

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
                                          disabled={loading || !city?.id}
                                          className={`px-4 py-2 text-white rounded ${loading || !city?.id ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"}`}
                                    >
                                          {loading ? "Updating..." : "Update"}
                                    </button>
                              </div>
                        </form>
                  </div>
            </div>
      );
};

export default UpdateCityModal;
