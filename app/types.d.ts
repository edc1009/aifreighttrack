// Types for Google Analytics
interface Window {
  gtag: (
    command: 'event',
    action: string,
    params: {
      [key: string]: any;
    }
  ) => void;
} 