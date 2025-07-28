#!/usr/bin/env python3
"""
Main Entry Point for Adobe Hackathon - Optimized PDF Outline Extractor
Includes performance monitoring and stream-based processing.
"""

import sys
import time
import json
from pathlib import Path

# Optimized processing components
from src.performance_optimizer import FastPDFProcessor, ResourceMonitor


def process_pdfs(input_dir: Path, output_dir: Path) -> None:
    """
    Process all PDF files in the input directory using optimized components.
    
    Args:
        input_dir (Path): Directory containing input PDF files.
        output_dir (Path): Directory to store output JSON files.
    """
    # Initialize resource monitoring
    monitor = ResourceMonitor()
    monitor.start_monitoring()

    # Gather PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in the input directory.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Starting optimized processing...")

    # Initialize optimized processor
    processor = FastPDFProcessor()

    success_count = 0
    total_pages = 0

    for pdf_file in pdf_files:
        try:
            start_time = time.time()

            # Process PDF using streaming for performance
            result = processor.stream_process_pdf(str(pdf_file))

            # Output result
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            elapsed = time.time() - start_time
            pages = len(result.get('outline', [])) or 1
            total_pages += pages

            print(f"Processed: {pdf_file.name} in {elapsed:.2f} seconds ({pages} page(s))")

            if elapsed > 10 and pages <= 50:
                print(f"Warning: Processing time of {elapsed:.2f}s may be too slow for {pages} page(s).")

            success_count += 1

        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")

    # Generate and print performance report
    report = monitor.get_performance_report()
    report['pages_processed'] = total_pages

    print("\nProcessing Summary")
    print(f"Files successfully processed: {success_count}/{len(pdf_files)}")
    print(f"Total pages processed: {total_pages}")
    print(f"Total elapsed time: {report['elapsed_time']:.2f} seconds")
    print(f"Peak memory usage: {report['peak_memory_mb']:.1f} MB")
    print(f"Average time per page: {report['time_per_page']:.3f} seconds")

    # Check performance compliance
    if report['memory_compliant'] and report['time_per_page'] < 0.2:
        print("Performance constraints satisfied.")
    else:
        print("Performance constraints not met. Optimization may be required.")


def main():
    """
    Main entry point: Validates input/output directories and invokes the processing pipeline.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not input_dir.exists():
        print(f"Input directory does not exist: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    process_pdfs(input_dir, output_dir)


if __name__ == "__main__":
    main()
