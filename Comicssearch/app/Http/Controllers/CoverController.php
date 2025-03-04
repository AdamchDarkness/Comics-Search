<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class CoverController extends Controller
{
    /**
     * Renvoie l'image demandée depuis le NAS.
     *
     * @param string $filename Le nom du fichier d'image (encodé dans l'URL)
     * @return \Symfony\Component\HttpFoundation\BinaryFileResponse|\Illuminate\Http\Response
     */
    public function getCover($filename)
    {

        $filename = urldecode($filename);


        $filePath = '\\\\lord_of_adam\\Comics Mangas Livre\\Comics\\extracted_covers\\' . $filename;
        
        if (!file_exists($filePath)) {
            abort(404, 'Image not found.');
        }

        $mimeType = mime_content_type($filePath) ?: 'image/png';

        return response()->file($filePath, [
            'Content-Type' => $mimeType
        ]);
    }
}
