import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'https://textforge-ai-backend.onrender.com';

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
    // State for file upload mode
    const [uploadMode, setUploadMode] = useState(false);
    // State for selected file
    const [selectedFile, setSelectedFile] = useState(null);
    // State for file upload result
    const [fileResult, setFileResult] = useState(null);

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
     * Calls the backend API for text processing.
     * @param {string} featureType - The type of text processing to perform.
     * @returns {Promise<string>} A promise that resolves with the processed text or rejects with an error.
     */
    const callBackendApi = async (featureType) => {
        const apiEndpoints = {
            'paraphrase': '/paraphrase',
            'grammar_check': '/grammar',
            'plagiarism_check': '/plagiarism',
            'summarize': '/summarize'
        };

        const endpoint = apiEndpoints[featureType];
        if (!endpoint) {
            throw new Error('Unknown feature requested.');
        }

        try {
            let requestData;
            if (featureType === 'plagiarism_check') {
                requestData = {
                    text: inputText,
                    reference_texts: [] // Using default reference texts from backend
                };
            } else {
                requestData = { text: inputText };
            }

            const response = await axios.post(`${API_BASE_URL}${endpoint}`, requestData);
            
            // Extract the relevant result based on feature type
            switch (featureType) {
                case 'paraphrase':
                    return response.data.paraphrased;
                case 'grammar_check':
                    return response.data.corrected;
                case 'summarize':
                    return response.data.summary;
                case 'plagiarism_check':
                    return response.data.message;
                default:
                    return JSON.stringify(response.data);
            }
        } catch (error) {
            console.error(`API error for ${featureType}:`, error);
            if (error.response) {
                throw new Error(`Server error: ${error.response.status} - ${error.response.data?.detail || error.response.statusText}`);
            } else if (error.request) {
                throw new Error('Network error: Could not connect to the backend server.');
            } else {
                throw new Error(`Request error: ${error.message}`);
            }
        }
    };

    /**
     * Generic handler for all feature buttons.
     * @param {string} feature - The feature to activate.
     */
    const handleFeatureClick = async (feature) => {
        if (!inputText.trim()) {
            setErrorMessage('Please enter some text before processing.');
            return;
        }

        setErrorMessage(''); // Clear previous errors
        setOutputText(''); // Clear previous output
        setActiveFeature(feature); // Set active feature for UI feedback
        setIsLoading(true); // Start loading

        try {
            const result = await callBackendApi(feature);
            setOutputText(result);
        } catch (error) {
            setErrorMessage(`Error: ${error.message}`);
            console.error(`Error processing ${feature}:`, error);
        } finally {
            setIsLoading(false); // End loading
            setActiveFeature(''); // Reset active feature
        }
    };

    /**
     * Handles file selection
     * @param {Object} e - The event object from the file input
     */
    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setErrorMessage('');
            setFileResult(null);
            setOutputText('');
        }
    };

    /**
     * Handles file upload and processing
     * @param {string} feature - The feature to use for processing the file
     */
    const handleFileUpload = async (feature) => {
        if (!selectedFile) {
            setErrorMessage('Please select a file first.');
            return;
        }

        setErrorMessage('');
        setOutputText('');
        setFileResult(null);
        setActiveFeature(feature);
        setIsLoading(true);

        const uploadEndpoints = {
            'paraphrase': '/upload/paraphrase',
            'grammar_check': '/upload/grammar',
            'plagiarism_check': '/upload/plagiarism',
            'summarize': '/upload/summarize'
        };

        const endpoint = uploadEndpoints[feature];
        if (!endpoint) {
            setErrorMessage('Unknown feature requested.');
            setIsLoading(false);
            setActiveFeature('');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', selectedFile);

            const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setFileResult(response.data);
            
            // Extract the relevant result based on feature type
            let result = '';
            switch (feature) {
                case 'paraphrase':
                    result = response.data.paraphrased;
                    break;
                case 'grammar_check':
                    result = response.data.corrected;
                    break;
                case 'summarize':
                    result = response.data.summary;
                    break;
                case 'plagiarism_check':
                    result = response.data.message;
                    break;
                default:
                    result = JSON.stringify(response.data);
            }
            
            setOutputText(result);
            setInputText(response.data.original_text || ''); // Show original text in input
            
        } catch (error) {
            console.error(`File upload error for ${feature}:`, error);
            if (error.response) {
                const detail = error.response.data?.detail || error.response.statusText;
                setErrorMessage(`Server error: ${error.response.status} - ${detail}`);
            } else if (error.request) {
                setErrorMessage('Network error: Could not connect to the backend server.');
            } else {
                setErrorMessage(`Request error: ${error.message}`);
            }
        } finally {
            setIsLoading(false);
            setActiveFeature('');
        }
    };

    /**
     * Toggle between text input and file upload modes
     */
    const toggleUploadMode = () => {
        setUploadMode(!uploadMode);
        setSelectedFile(null);
        setFileResult(null);
        setInputText('');
        setOutputText('');
        setErrorMessage('');
    };

    return (
        <div className="app-container">
            <div className="main-card">
                {/* Header */}
                <h1 className="app-title">
                    <span className="gradient-text">
                        TextForge AI
                    </span>
                </h1>
                <p className="app-subtitle">
                    Your all-in-one tool for intelligent text processing: Paraphrase, Grammar Check, Plagiarism Detection, and Summarization.
                </p>

                {/* Mode Toggle */}
                <div className="mode-toggle-container">
                    <button 
                        onClick={toggleUploadMode}
                        className={`mode-toggle-button ${!uploadMode ? 'active' : ''}`}>
                        Text Input
                    </button>
                    <button 
                        onClick={toggleUploadMode}
                        className={`mode-toggle-button ${uploadMode ? 'active' : ''}`}>
                        File Upload
                    </button>
                </div>

                {/* Input Section */}
                {uploadMode ? (
                    <div className="input-section file-upload-section">
                        <label htmlFor="fileUpload" className="input-label">
                            Upload a File (.txt, .md, .pdf):
                        </label>
                        <div className="file-input-container">
                            <input
                                id="fileUpload"
                                type="file"
                                accept=".txt,.md,.pdf"
                                onChange={handleFileSelect}
                                className="file-input"
                            />
                            <label htmlFor="fileUpload" className="file-input-label">
                                {selectedFile ? (
                                    <div className="file-selected">
                                        <div className="file-icon">
                                            {selectedFile.name.endsWith('.pdf') ? '📄' : '📝'}
                                        </div>
                                        <div className="file-info">
                                            <div className="file-name">{selectedFile.name}</div>
                                            <div className="file-size">{(selectedFile.size / 1024).toFixed(1)} KB</div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="file-placeholder">
                                        <div className="upload-icon">📁</div>
                                        <div>Choose a file to upload...</div>
                                        <div className="file-types">Supports: .txt, .md, .pdf</div>
                                    </div>
                                )}
                            </label>
                        </div>
                    </div>
                ) : (
                    <div className="input-section">
                        <label htmlFor="inputText" className="input-label">
                            Enter Your Text Here:
                        </label>
                        <textarea
                            id="inputText"
                            className="input-textarea"
                            placeholder="Type or paste your text here..."
                            value={inputText}
                            onChange={handleInputChange}
                            rows="8"
                        ></textarea>
                    </div>
                )}

                {/* Feature Buttons */}
                <div className="buttons-grid">
                    <button
                        onClick={() => uploadMode ? handleFileUpload('paraphrase') : handleFeatureClick('paraphrase')}
                        className={`feature-button button-paraphrase ${isLoading && activeFeature === 'paraphrase' ? 'button-paraphrase' : ''}`}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'paraphrase' ? (
                            <span className="loading-spinner">
                                <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Paraphrasing...
                            </span>
                        ) : 'Paraphrase'}
                    </button>

                    <button
                        onClick={() => uploadMode ? handleFileUpload('grammar_check') : handleFeatureClick('grammar_check')}
                        className={`feature-button button-grammar ${isLoading && activeFeature === 'grammar_check' ? 'button-grammar' : ''}`}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'grammar_check' ? (
                            <span className="loading-spinner">
                                <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Checking...
                            </span>
                        ) : 'Grammar Check'}
                    </button>

                    <button
                        onClick={() => uploadMode ? handleFileUpload('plagiarism_check') : handleFeatureClick('plagiarism_check')}
                        className={`feature-button button-plagiarism ${isLoading && activeFeature === 'plagiarism_check' ? 'button-plagiarism' : ''}`}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'plagiarism_check' ? (
                            <span className="loading-spinner">
                                <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Scanning...
                            </span>
                        ) : 'Plagiarism Check'}
                    </button>

                    <button
                        onClick={() => uploadMode ? handleFileUpload('summarize') : handleFeatureClick('summarize')}
                        className={`feature-button button-summarize ${isLoading && activeFeature === 'summarize' ? 'button-summarize' : ''}`}
                        disabled={isLoading}
                    >
                        {isLoading && activeFeature === 'summarize' ? (
                            <span className="loading-spinner">
                                <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 818-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Summarizing...
                            </span>
                        ) : 'Summarize'}
                    </button>
                </div>

                {/* Output Section */}
                <div className="output-section">
                    <label htmlFor="outputText" className="output-label">
                        Result:
                    </label>
                    {errorMessage && (
                        <div className="error-message" role="alert">
                            <strong className="error-title">Error!</strong>
                            <span className="error-text">{errorMessage}</span>
                        </div>
                    )}
                    <textarea
                        id="outputText"
                        className="output-textarea"
                        placeholder="Your processed text will appear here..."
                        value={outputText}
                        readOnly
                        rows="8"
                    ></textarea>
                </div>
            </div>
        </div>
    );
};

export default App;
