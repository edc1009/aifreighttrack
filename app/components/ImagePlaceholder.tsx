'use client';

interface ImagePlaceholderProps {
  companyName: string;
  width: number;
  height: number;
}

export default function ImagePlaceholder({ companyName, width, height }: ImagePlaceholderProps) {
  // Get first letter of each word as initials
  const initials = companyName
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase();

  return (
    <div 
      style={{ 
        width: `${width}px`, 
        height: `${height}px`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#e5e7eb',
        borderRadius: '4px',
        fontSize: `${Math.floor(height / 2)}px`,
        fontWeight: 'bold',
        color: '#4b5563'
      }}
    >
      {initials}
    </div>
  );
} 