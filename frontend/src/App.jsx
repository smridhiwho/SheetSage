import React, { useState, useEffect } from "react";
import { FaPen, FaTrashAlt } from "react-icons/fa";

function App() {
  const [spreadsheetLink, setSpreadsheetLink] = useState("");
  const [promptInput, setPromptInput] = useState("");
  const [promptExcel, setPromptExcel] = useState("");
  const [embedLink, setEmbedLink] = useState("");
  const [history, setHistory] = useState(() => {
    const savedHistory = localStorage.getItem("sheetHistory");
    return savedHistory ? JSON.parse(savedHistory) : [];
  });

  useEffect(() => {
    localStorage.setItem("sheetHistory", JSON.stringify(history));
  }, [history]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (spreadsheetLink.includes("docs.google.com/spreadsheets")) {
      const embedUrl = spreadsheetLink.replace("/edit", "/pubhtml");
      const sheetName = promptInput || `Sheet ${history.length + 1}`;

      setEmbedLink(embedUrl);

      const newHistory = [
        ...history,
        { id: Date.now(), name: sheetName, link: embedUrl },
      ];

      setHistory(newHistory);
      setSpreadsheetLink("");
      setPromptInput("");

      // Send the spreadsheet link and prompt input to the backend
      try {
        const response = await fetch(
          "http://localhost:5000/log_spreadsheet_id",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              spreadsheetLink,
              promptExcel, // Include the prompt input in the request
            }),
          }
        );

        const result = await response.json();
        if (response.ok) {
          console.log("Data logged successfully:", result);
        } else {
          console.error("Error logging data:", result.error);
        }
      } catch (error) {
        console.error("Error communicating with backend:", error);
      }
    } else {
      alert("Please enter a valid Google Sheets link.");
    }
  };

  const handleSheetClick = (link) => {
    setEmbedLink(link);
  };

  const handleDelete = (id) => {
    const updatedHistory = history.filter((sheet) => sheet.id !== id);
    setHistory(updatedHistory);
  };

  const handleRename = (id) => {
    const newName = window.prompt("Enter new name for the sheet:");
    if (newName) {
      const updatedHistory = history.map((sheet) =>
        sheet.id === id ? { ...sheet, name: newName } : sheet
      );
      setHistory(updatedHistory);
    }
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-r from-[#4a90e2] to-[#6dbaff]">
      {/* Sidebar */}
      <aside className="w-64 bg-gradient-to-b from-[#4a90e2] to-[#6dbaff] p-6 shadow-lg rounded-lg">
        <h2 className="text-2xl font-bold text-white mb-6">Sheets History</h2>
        <ul className="space-y-4">
          {history.map((sheet) => (
            <li
              key={sheet.id}
              className="p-3 bg-[#4a90e2] rounded-lg hover:bg-[#357ab7] text-white flex justify-between items-center transition-colors"
            >
              <span
                className="cursor-pointer flex-grow hover:text-yellow-300"
                onClick={() => handleSheetClick(sheet.link)}
              >
                {sheet.name}
              </span>
              <div className="flex space-x-2">
                <button
                  className="text-yellow-300 hover:text-yellow-500 transition"
                  onClick={() => handleRename(sheet.id)}
                >
                  <FaPen />
                </button>
                <button
                  className="text-red-400 hover:text-red-600 transition"
                  onClick={() => handleDelete(sheet.id)}
                >
                  <FaTrashAlt />
                </button>
              </div>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main Content */}
      <main className="flex-grow p-8 bg-gradient-to-b from-white to-gray-100">
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-lg shadow-xl w-full max-w-lg mx-auto"
        >
          <h2 className="text-3xl font-semibold text-gray-800 mb-4">
            SheetSage 🧙‍♂️
          </h2>
          <div className="mb-4">
            <label
              htmlFor="spreadsheetLink"
              className="block text-lg font-medium text-gray-700 mb-2"
            >
              Spreadsheet Link
            </label>
            <input
              id="spreadsheetLink"
              type="text"
              placeholder="Enter Google Sheets link"
              className="w-full p-3 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              value={spreadsheetLink}
              onChange={(e) => setSpreadsheetLink(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="promptInput"
              className="block text-lg font-medium text-gray-700 mb-2"
            >
              Sheet Name - Optional
            </label>
            <input
              id="promptInput"
              type="text"
              placeholder="Enter a name for the sheet"
              className="w-full p-3 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              value={promptInput}
              onChange={(e) => setPromptInput(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="promptExcel"
              className="block text-lg font-medium text-gray-700 mb-2"
            >
              Prompt
            </label>
            <input
              id="promptExcel"
              type="text"
              placeholder="Enter the work you want to get done with the sheet."
              className="w-full p-3 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              value={promptExcel}
              onChange={(e) => setPromptExcel(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-[#4a90e2] to-[#6dbaff] text-white py-3 rounded-md hover:from-[#357ab7] hover:to-[#7fc4ff] transition"
          >
            Submit
          </button>
        </form>

        {embedLink && (
          <div className="mt-8">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">
              Embedded Spreadsheet
            </h3>
            <iframe
              src={embedLink}
              width="100%"
              height="400px"
              className="border-2 border-gray-300 rounded-lg shadow-xl"
              title="Embedded Google Sheet"
            ></iframe>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
