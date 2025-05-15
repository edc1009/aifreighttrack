'use client';

import { useState } from 'react';
import { shippingCompanies } from '../utils/shippingCompanies';
import Image from 'next/image';
import ImagePlaceholder from './ImagePlaceholder';

export default function ShippingCompanyGrid() {
  const [imageError, setImageError] = useState<Record<string, boolean>>({});

  const handleImageError = (companyName: string) => {
    setImageError(prev => ({
      ...prev,
      [companyName]: true
    }));
  };

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4 text-center">Supported Shipping Companies</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {shippingCompanies.map((company, index) => (
          <div key={index} className="flex flex-col items-center p-4 border rounded-lg bg-white shadow-sm">
            <div className="h-16 w-16 relative flex items-center justify-center mb-2">
              {imageError[company.name] ? (
                <ImagePlaceholder companyName={company.name} width={64} height={64} />
              ) : (
                <Image
                  src={`/images/${company.logo}`}
                  alt={`${company.name} logo`}
                  width={64}
                  height={64}
                  style={{ objectFit: 'contain' }}
                  onError={() => handleImageError(company.name)}
                />
              )}
            </div>
            <span className="text-sm font-medium text-center">{company.name}</span>
            <span className="text-xs text-gray-500">{company.codes.join(', ')}</span>
          </div>
        ))}
      </div>
    </div>
  );
} 