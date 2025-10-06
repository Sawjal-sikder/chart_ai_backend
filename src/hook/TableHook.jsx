import React from "react";

const ReusableTable = ({ columns, data, actions }) => {
      return (
            <div className="bg-white shadow rounded-lg overflow-hidden">
                  <table className="table-auto w-full border-collapse">
                        <thead>
                              <tr className="bg-[#fafafa] text-center border-b">
                                    {columns.map((col, idx) => (
                                          <th
                                                key={idx}
                                                className="px-4 py-5 text-center font-semibold text-gray-700"
                                          >
                                                {col.header}
                                          </th>
                                    ))}
                                    {actions && (
                                          <th className="px-4 py-5 font-semibold text-gray-700">Action</th>
                                    )}
                              </tr>
                        </thead>
                        <tbody>
                              {data?.map((row, rowIndex) => (
                                    <tr
                                          key={row.id || rowIndex}
                                          className="hover:bg-gray-50 transition-colors border-b last:border-b-0"
                                    >
                                          {columns.map((col, colIndex) => (
                                                <td key={colIndex} className="px-4 py-5 ">
                                                      {col.render ? col.render(row, rowIndex) : (row[col.accessor] || row[col.accessor] === 0 ? row[col.accessor] : "-")}
                                                </td>
                                          ))}
                                          {actions && (
                                                <td className="px-4 py-5 flex gap-5 justify-center">
                                                      {actions.map((action, i) => (
                                                            <button
                                                                  key={i}
                                                                  className={`${action.className} flex items-center gap-1`}
                                                                  onClick={() => action.onClick(row)}
                                                            >
                                                                  {action.icon} {action.label}
                                                            </button>
                                                      ))}
                                                </td>
                                          )}
                                    </tr>
                              ))}
                        </tbody>
                  </table>
            </div>
      );
};

export default ReusableTable;
