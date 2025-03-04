<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Elastic\Elasticsearch\ClientBuilder;

class SearchController extends Controller
{
    protected $client;

    public function __construct()
    {
        
        $this->client = ClientBuilder::create()
            ->setHosts(['https://localhost:9200'])
            ->setBasicAuthentication('elastic', 'lOf0*vttz9GwK3yUJhU=')
            ->setSSLVerification(false) 
            ->build();
    }


    public function search(Request $request)
    {
        $queryText = $request->input('query', '');
        $saga      = $request->input('saga', '');
        $extention = $request->input('extention', '');
        $maison    = $request->input('maison_d_edition', '');
        $run       = $request->input('run', '');

        $mustQuery = [];
        if (empty($queryText)) {
           
            $mustQuery[] = ['match_all' => new \stdClass()];
        } else {
            $mustQuery[] = [
                'multi_match' => [
                    'query'  => $queryText,
                    'fields' => ['nom', 'titre_saga']
                ]
            ];
        }

        
        $params = [
            'index' => 'comics',
            'body'  => [
                'size'  => 300,
                'query' => [
                    'bool' => [
                        'must'   => $mustQuery,
                        'filter' => []
                    ]
                ]
            ]
        ];

        
        if (!empty($saga)) {
            $params['body']['query']['bool']['filter'][] = ['term' => ['saga' => $saga]];
        }
        if (!empty($extention)) {
            $params['body']['query']['bool']['filter'][] = ['term' => ['extention' => $extention]];
        }
        if (!empty($maison)) {
            $params['body']['query']['bool']['filter'][] = ['term' => ['maison_d_edition' => $maison]];
        }
        if (!empty($run)) {
            $params['body']['query']['bool']['filter'][] = ['term' => ['run' => $run]];
        }

        $results = $this->client->search($params);
        
        return response()->json($results->asArray());
    }
}
