export interface ShippingCompany {
  name: string;
  codes: string[];
  logo: string;
  blUrl: string;
  containerUrl: string;
}

export const shippingCompanies: ShippingCompany[] = [
  {
    name: 'Maersk',
    codes: ['MAEU'],
    logo: 'maersk.png',
    blUrl: 'https://www.maersk.com/tracking/#tracking/',
    containerUrl: 'https://www.maersk.com/tracking/#tracking/',
  },
  {
    name: 'COSCO',
    codes: ['COSU'],
    logo: 'cosco.png',
    blUrl: 'https://elines.coscoshipping.com/ebusiness/cargotracking',
    containerUrl: 'https://elines.coscoshipping.com/ebusiness/cargotracking',
  },
  {
    name: 'Wan Hai',
    codes: ['WHLC'],
    logo: 'wanhai.png',
    blUrl: 'https://www.wanhai.com/views/CargoTracking/CargoTracking.xhtml',
    containerUrl: 'https://www.wanhai.com/views/CargoTracking/CargoTracking.xhtml',
  },
  {
    name: 'SeaLead',
    codes: ['SEAU'],
    logo: 'sealead.png',
    blUrl: 'https://www.sealead.com/en/tools/track-shipment/',
    containerUrl: 'https://www.sealead.com/en/tools/track-shipment/',
  },
  {
    name: 'HMM',
    codes: ['HDMU'],
    logo: 'hmm.png',
    blUrl: 'https://www.hmm21.com/cms/business/e_service/cargo_tracking/index.jsp',
    containerUrl: 'https://www.hmm21.com/cms/business/e_service/cargo_tracking/index.jsp',
  },
  {
    name: 'MSC',
    codes: ['MSCU'],
    logo: 'msc.png',
    blUrl: 'https://www.msc.com/track-a-shipment',
    containerUrl: 'https://www.msc.com/track-a-shipment',
  },
  {
    name: 'ONE',
    codes: ['ONEU'],
    logo: 'one.png',
    blUrl: 'https://ecomm.one-line.com/ecom/CUP_HOM_3301.do',
    containerUrl: 'https://ecomm.one-line.com/ecom/CUP_HOM_3301.do',
  },
  {
    name: 'ZIM',
    codes: ['ZIMU'],
    logo: 'zim.png',
    blUrl: 'https://www.zim.com/tools/track-a-shipment',
    containerUrl: 'https://www.zim.com/tools/track-a-shipment',
  },
  {
    name: 'Yang Ming',
    codes: ['YMLU'],
    logo: 'yangming.png',
    blUrl: 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx',
    containerUrl: 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx',
  },
  {
    name: 'OOCL',
    codes: ['OOLU'],
    logo: 'oocl.png',
    blUrl: 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx',
    containerUrl: 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx',
  },
  {
    name: 'Hapag-Lloyd',
    codes: ['HLCU'],
    logo: 'hlcu.png',
    blUrl: 'https://www.hapag-lloyd.com/en/online-business/track/track-by-booking-solution.html',
    containerUrl: 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html',
  },
  {
    name: 'CMA CGM',
    codes: ['CMDU'],
    logo: 'cmdu.png',
    blUrl: 'https://www.cma-cgm.com/ebusiness/tracking',
    containerUrl: 'https://www.cma-cgm.com/ebusiness/tracking',
  },
  {
    name: 'Evergreen',
    codes: ['EGLV'],
    logo: 'eglv.png',
    blUrl: 'https://www.evergreen-line.com/cargo-tracking',
    containerUrl: 'https://www.evergreen-line.com/cargo-tracking',
  },
];

// Validate container number format (4 letters ending with U + 7 digits)
export const isValidContainerNumber = (containerNumber: string): boolean => {
  const pattern = /^[A-Z]{3}U\d{7}$/;
  return pattern.test(containerNumber);
};

// Basic validation for BL number format
export const isValidBLNumber = (blNumber: string): boolean => {
  return blNumber.trim().length > 0;
};

// Detect shipping company based on container or BL number
export const detectShippingCompany = (number: string, type: 'container' | 'bl'): ShippingCompany | null => {
  // For containers, check prefix
  if (type === 'container' && number.length >= 4) {
    const prefix = number.substring(0, 4);
    
    for (const company of shippingCompanies) {
      if (company.codes.some(code => prefix.startsWith(code.substring(0, 3)))) {
        return company;
      }
    }
  }
  
  // For BL numbers, check if starts with any code
  if (type === 'bl') {
    for (const company of shippingCompanies) {
      if (company.codes.some(code => number.startsWith(code))) {
        return company;
      }
    }
  }
  
  return null;
};

// Get redirect URL based on shipping company and number type
export const getRedirectUrl = (
  company: ShippingCompany,
  number: string,
  type: 'container' | 'bl'
): string => {
  const baseUrl = type === 'container' ? company.containerUrl : company.blUrl;
  
  // Here you would add the specific URL parameter structure for each company
  // For now, we'll use a generic approach
  if (baseUrl.includes('?')) {
    return `${baseUrl}&${type}=${number}`;
  } else {
    return `${baseUrl}?${type}=${number}`;
  }
}; 