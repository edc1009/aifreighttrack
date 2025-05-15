import SearchForm from './components/SearchForm';
import ShippingCompanyGrid from './components/ShippingCompanyGrid';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-12 px-4">
        <header className="text-center mb-12">
          <h1 className="text-3xl font-bold mb-2">Container/BL Redirect Tracker</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Track your shipments across multiple shipping lines. Enter your Container Number or Bill of Lading Number to be redirected to the right shipping company.
          </p>
        </header>

        <SearchForm />
        
        <ShippingCompanyGrid />
      </div>
      
      <footer className="py-6 mt-12 bg-white border-t">
        <div className="container mx-auto px-4">
          <p className="text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} Container/BL Redirect Tracker. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
} 