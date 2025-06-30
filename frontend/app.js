import React, { useState } from 'react';

// Main App component
const App = () => {
    // State to hold the user's input text
    const [inputText, setInputText] = useState('');
    // State to hold the processed output text
    const [outputText, setOutputText] = useState('');
    // State to manage the currently active feature (e.g., 'paraphrase', 'grammar')
    const [activeFeature, setActiveFeature] = useState('');
    // State to show/hide loading indicator
    const [isLoading, setIsLoading] = useState(false);
    // State to store and display error messages
    const [errorMessage, setErrorMessage] = useState('');

    /**
     * Handles the change event for the input text area.
     * @param {Object} e - The event object from the textarea.
     */
    const handleInputChange = (e) => {
        setInputText(e.target.value);
        // Clear previous output and error when input changes
        setOutputText('');
        setErrorMessage('');
    };

    /**
     * Simulates an API call to a backend service.
     * In a real application, you would replace this with actual fetch/axios calls
     * to your Python backend.
     * @param {string} featureType - The type of text processing to perform (e.g., 'paraphrase').
     * @returns {Promise<string>} A promise that resolves with the processed text or rejects with an error.
     */
    const callBackendApi = async (featureType) => {
        // Placeholder for your backend API endpoint
        // In a real app, this would be something like: 'http://localhost:5000/paraphrase'
        const apiUrl = `/api/${featureType}`; // Example path

        // Simulate network delay and processing
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (inputText.trim() === '') {
                    // Reject if input is empty
                    reject('Input text cannot be empty.');
                    return;
                }

                let simulatedResult;
                switch (featureType) {
                    case 'paraphrase':
                        simulatedResult = `This is a paraphrased version of: "${inputText}". Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla.`;
                        break;
                    case 'grammar_check':
                        // Simple grammar check simulation
                        if (inputText.includes('I is')) {
                            simulatedResult = `Corrected: "${inputText.replace('I is', 'I am')}". Suggested changes: Change 'is' to 'am'.`;
                        } else {
                            simulatedResult = `Grammar check complete. No significant issues found for: "${inputText}".`;
                        }
                        break;
                    case 'plagiarism_check':
                        // Simple plagiarism check simulation
                        if (inputText.includes('To be or not to be')) {
                            simulatedResult = `Plagiarism detected! This text contains highly similar phrases to known works. Original source: "Hamlet" by William Shakespeare.`;
                        } else {
                            simulatedResult = `Plagiarism check complete. No significant plagiarism found for: "${inputText}".`;
                        }
                        break;
                    case 'summarize':
                        const words = inputText.split(/\s+/);
                        const summaryLength = Math.max(5, Math.floor(words.length * 0.3)); // 30% of words, min 5
                        simulatedResult = `Summary of "${inputText.substring(0, 50)}...": ${words.slice(0, summaryLength).join(' ')}. This is a condensed version of your original text, focusing on key points.`;
                        break;
                    default:
                        reject('Unknown feature requested.');
                        return;
                }
                resolve(simulatedResult);
            }, 1500); // Simulate 1.5 seconds of loading
        });
    };

    /**
     * Generic handler for all feature buttons.
     * @param {string} feature - The feature to activate ('paraphrase', 'grammar_check', 'plagiarism_check', 'summarize').
     */
    const handleFeatureClick = async (feature) => {
        setErrorMessage(''); // Clear previous errors
        setOutputText(''); // Clear previous output
        setActiveFeature(feature); // Set active feature for UI feedback
        setIsLoading(true); // Start loading

        try {
            const result = await callBackendApi(feature);
            setOutputText(result);
        } catch (error) {
            setErrorMessage(`Error: ${error}`);
            console.error(`Error processing ${feature}:`, error);
        } finally {
            setIsLoading(false); // End loading
            setActiveFeature(''); // Reset active feature
        }
    };

    return (
        // Main container using Tailwind CSS for responsiveness and centering
        <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-4 font-inter">
            <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12 w-full max-w-4xl transform transition-all duration-300 ease-in-out hover:scale-[1.01]">
                {/* Header */}
                <h1 className="text-4xl md:text-5xl font-extrabold text-center text-gray-900 mb-8 tracking-tight">
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-500">
                        TextForge AI
                    </span>
                </h1>
                <p className="text-center text-gray-600 mb-10 text-lg md:text-xl max-w-2xl mx-auto">
                    Your all-in-one tool for intelligent text processing: Paraphrase, Grammar Check, Plagiarism Detection, and Summarization.
                </p>

                {/* Input Section */}
                <div className="mb-8">
                    <label htmlFor="inputText" className="block text-xl font-semibold text-gray-800 mb-3">
                        Enter Your Text Here:
                    </label>
                    <textarea
                        id="inputText"
                        className="w-full p-4 border border-gray-300 rounded-xl focus:ring-4 focus:ring-blue-200 focus:border-blue-500 transition-all duration-200 ease-in-out text-lg resize-y min-h-[150px] shadow-sm"
                        placeholder="Type or paste your text here..."
                        value={inputText}
                        onChange={handleInputChange}
                        rows="8"
                    ></textarea>
                </div>

                {/* Feature Buttons */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <button
                        onClick={() => handleFeatureClick('paraphrase')}
                        className={`
                            w-full py-3 px-6 rounded-xl text-lg font-semibold transition-all duration-300 ease-in-out shadow-md
                            ${isLoading && activeFeature === 'paraphrase' ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white hover:shadow-lg'}
                            focus:outline-none focus:ring-4 focus:ring-blue-300
                        `}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'paraphrase' ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Paraphrasing...
                            </span>
                        ) : 'Paraphrase'}
                    </button>

                    <button
                        onClick={() => handleFeatureClick('grammar_check')}
                        className={`
                            w-full py-3 px-6 rounded-xl text-lg font-semibold transition-all duration-300 ease-in-out shadow-md
                            ${isLoading && activeFeature === 'grammar_check' ? 'bg-green-300 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600 text-white hover:shadow-lg'}
                            focus:outline-none focus:ring-4 focus:ring-green-300
                        `}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'grammar_check' ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Checking...
                            </span>
                        ) : 'Grammar Check'}
                    </button>

                    <button
                        onClick={() => handleFeatureClick('plagiarism_check')}
                        className={`
                            w-full py-3 px-6 rounded-xl text-lg font-semibold transition-all duration-300 ease-in-out shadow-md
                            ${isLoading && activeFeature === 'plagiarism_check' ? 'bg-red-300 cursor-not-allowed' : 'bg-red-500 hover:bg-red-600 text-white hover:shadow-lg'}
                            focus:outline-none focus:ring-4 focus:ring-red-300
                        `}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'plagiarism_check' ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Scanning...
                            </span>
                        ) : 'Plagiarism Check'}
                    </button>

                    <button
                        onClick={() => handleFeatureClick('summarize')}
                        className={`
                            w-full py-3 px-6 rounded-xl text-lg font-semibold transition-all duration-300 ease-in-out shadow-md
                            ${isLoading && activeFeature === 'summarize' ? 'bg-yellow-300 cursor-not-allowed' : 'bg-yellow-500 hover:bg-yellow-600 text-white hover:shadow-lg'}
                            focus:outline-none focus:ring-4 focus:ring-yellow-300
                        `}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'summarize' ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Summarizing...
                            </span>
                        ) : 'Summarize'}
                    </button>
                </div>

                {/* Output Section */}
                <div className="relative">
                    <label htmlFor="outputText" className="block text-xl font-semibold text-gray-800 mb-3">
                        Result:
                    </label>
                    {errorMessage && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl mb-4" role="alert">
                            <strong className="font-bold">Error!</strong>
                            <span className="block sm:inline ml-2">{errorMessage}</span>
                        </div>
                    )}
                    <textarea
                        id="outputText"
                        className="w-full p-4 border border-gray-300 rounded-xl bg-gray-50 text-gray-700 text-lg resize-y min-h-[150px] shadow-sm"
                        placeholder="Your processed text will appear here..."
                        value={outputText}
                        readOnly // Output is read-only
                        rows="8"
                    ></textarea>
                </div>
            </div>
        </div>
    );
};

export default App;
