'use client';

import { useState } from 'react';
import { 
  detectShippingCompany, 
  isValidContainerNumber, 
  isValidBLNumber, 
  getRedirectUrl 
} from '../utils/shippingCompanies';
import ErrorMessage from './ErrorMessage';

type SearchType = 'container' | 'bl';

export default function SearchForm() {
  const [searchType, setSearchType] = useState<SearchType>('container');
  const [searchValue, setSearchValue] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Normalize input - remove spaces and convert to uppercase
    const normalizedValue = searchValue.replace(/\s+/g, '').toUpperCase();

    // Validate input format
    if (searchType === 'container' && !isValidContainerNumber(normalizedValue)) {
      setError('Invalid container number format. Please enter a valid container number (e.g., ABCDU1234567).');
      return;
    }

    if (searchType === 'bl' && !isValidBLNumber(normalizedValue)) {
      setError('Please enter a valid bill of lading number.');
      return;
    }

    // Detect shipping company
    const company = detectShippingCompany(normalizedValue, searchType);
    
    if (!company) {
      setError(`Could not identify a shipping company for this ${searchType === 'container' ? 'container' : 'BL'} number.`);
      return;
    }

    // Track the search in analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'search', {
        search_term: normalizedValue,
        search_type: searchType,
        shipping_company: company.name
      });
    }

    // Get the redirect URL and open in a new tab
    const redirectUrl = getRedirectUrl(company, normalizedValue, searchType);
    window.open(redirectUrl, '_blank');
  };

  return (
    <div className="w-full max-w-xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <form onSubmit={handleSearch} className="space-y-6">
        <div className="flex flex-col space-y-2">
          <div className="flex space-x-4">
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                name="searchType"
                value="container"
                checked={searchType === 'container'}
                onChange={() => setSearchType('container')}
              />
              <span className="ml-2">Container Number</span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                name="searchType"
                value="bl"
                checked={searchType === 'bl'}
                onChange={() => setSearchType('bl')}
              />
              <span className="ml-2">BL Number</span>
            </label>
          </div>
        </div>

        <div>
          <input
            type="text"
            placeholder={searchType === 'container' ? "Enter container number (e.g., ABCDU1234567)" : "Enter bill of lading number"}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            required
          />
        </div>

        {error && (
          <ErrorMessage message={error} onDismiss={() => setError(null)} />
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
        >
          Search
        </button>
      </form>
    </div>
  );
} 